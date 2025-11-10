"""
Ingestion router for document upload and indexing.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import logging
from typing import List
import uuid
from datetime import datetime

from app.core.txtai_client import txtai_client
from app.core.document_processor import document_processor
from app.core.s3_client import s3_client
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and index a document (PDF or Markdown).
    
    Returns:
        Indexing status and metadata
    """
    try:
        # Validate file type
        ext = file.filename.split('.')[-1].lower() if file.filename else ""

        if ext not in ["pdf", "md", "markdown"]:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {ext}. Supported: pdf, md, markdown"
            )

        # Read file content
        file_content = await file.read()

        # Generate document ID
        doc_id = str(uuid.uuid4())

        # Upload original document to S3
        try:
            # Determine content type
            content_type_map = {
                "pdf": "application/pdf",
                "md": "text/markdown",
                "markdown": "text/markdown"
            }
            content_type = content_type_map.get(ext, "application/octet-stream")

            s3_key = s3_client.upload_document(
                file_content=file_content,
                document_id=doc_id,
                filename=file.filename,
                content_type=content_type
            )
            logger.info(f"Document uploaded to S3: {s3_key}")
        except Exception as e:
            logger.error(f"Failed to upload document to S3: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to store document: {str(e)}"
            )

        # Process document based on type
        if ext == "pdf":
            text = document_processor.process_pdf(file_content, file.filename)
        elif ext in ["md", "markdown"]:
            text = document_processor.process_markdown(file_content, file.filename)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        # Chunk text
        chunks = document_processor.chunk_text(text)

        # Add document metadata to chunks
        indexed_chunks = []

        for chunk in chunks:
            chunk["id"] = f"{doc_id}_{chunk['id']}"
            chunk["metadata"].update({
                "filename": file.filename,
                "document_id": doc_id,
                "file_type": ext,
                "uploaded_at": datetime.utcnow().isoformat(),
                "s3_key": s3_key  # Store S3 location for reference
            })
            indexed_chunks.append(chunk)

        # Index chunks
        num_indexed = txtai_client.index_documents(indexed_chunks)

        return JSONResponse({
            "status": "indexed",
            "document_id": doc_id,
            "filename": file.filename,
            "s3_key": s3_key,
            "s3_bucket": settings.AWS_S3_BUCKET,
            "chunks": num_indexed,
            "total_chars": len(text)
        })
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error ingesting document: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")


@router.get("/stats")
async def get_index_stats():
    """Get indexing statistics."""
    try:
        stats = txtai_client.get_stats()
        return JSONResponse(stats)
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/document/{document_id}")
async def get_document(document_id: str):
    """
    Get presigned URL for downloading a document from S3.

    Args:
        document_id: The unique document identifier

    Returns:
        Presigned URL for temporary access to the document
    """
    try:
        # Note: This assumes we can reconstruct the S3 key from the document_id
        # In a production system, you might want to store the s3_key in a metadata database
        # For now, we'll return instructions on how to implement this properly
        raise HTTPException(
            status_code=501,
            detail="Document retrieval requires metadata storage (DynamoDB) to map document_id to s3_key. "
                   "Please implement metadata storage first."
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/document/download-url/{s3_key:path}")
async def get_download_url(s3_key: str, expiration: int = 3600):
    """
    Generate a presigned URL for downloading a document directly via S3 key.

    Args:
        s3_key: The S3 key (path) of the document
        expiration: Time in seconds for the URL to remain valid (default: 3600 = 1 hour)

    Returns:
        Presigned URL for temporary access to the document
    """
    try:
        # Validate expiration time
        if expiration < 60 or expiration > 604800:  # Between 1 minute and 7 days
            raise HTTPException(
                status_code=400,
                detail="Expiration must be between 60 and 604800 seconds (1 min to 7 days)"
            )

        # Check if document exists
        if not s3_client.document_exists(s3_key):
            raise HTTPException(
                status_code=404,
                detail=f"Document not found: {s3_key}"
            )

        # Generate presigned URL
        presigned_url = s3_client.generate_presigned_url(s3_key, expiration)

        # Get document metadata
        metadata = s3_client.get_document_metadata(s3_key)

        return JSONResponse({
            "download_url": presigned_url,
            "expires_in": expiration,
            "s3_key": s3_key,
            "metadata": metadata
        })

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating download URL: {e}")
        raise HTTPException(status_code=500, detail=str(e))

