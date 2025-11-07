"""
Retrieval router - decoupled from generation.
Returns relevant chunks and context for LLM.
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging

from app.core.txtai_client import txtai_client
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


class QueryRequest(BaseModel):
    question: str
    top_k: int = None


class QueryResponse(BaseModel):
    query: str
    context: str
    chunks: list
    top_k: int


@router.post("/query", response_model=QueryResponse)
async def retrieve_context(request: QueryRequest):
    """
    Retrieve relevant context chunks for a query.
    Decoupled from generation - returns context only.
    
    Returns:
        Retrieved chunks and formatted context
    """
    try:
        query = request.question
        top_k = request.top_k or settings.TOP_K_RESULTS
        
        # Semantic search
        results = txtai_client.search(query, limit=top_k)
        
        # Format context
        context_parts = []
        for result in results:
            context_parts.append(result["text"])
        
        context = "\n\n".join(context_parts)
        
        # Format with explicit boundaries (best practice)
        formatted_context = f"<context>\n{context}\n</context>"
        
        return JSONResponse({
            "query": query,
            "context": formatted_context,
            "chunks": results,
            "top_k": top_k
        })
        
    except Exception as e:
        logger.error(f"Error retrieving context: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving context: {str(e)}")

