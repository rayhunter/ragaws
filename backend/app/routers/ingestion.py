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
        doc_id = str(uuid.uuid4())
        indexed_chunks = []
        
        for chunk in chunks:
            chunk["id"] = f"{doc_id}_{chunk['id']}"
            chunk["metadata"].update({
                "filename": file.filename,
                "document_id": doc_id,
                "file_type": ext,
                "uploaded_at": datetime.utcnow().isoformat()
            })
            indexed_chunks.append(chunk)
        
        # Index chunks
        num_indexed = txtai_client.index_documents(indexed_chunks)
        
        return JSONResponse({
            "status": "indexed",
            "document_id": doc_id,
            "filename": file.filename,
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

