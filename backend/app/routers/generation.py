"""
Generation router - decoupled from retrieval.
Takes context and generates LLM response using AWS Bedrock.
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
from typing import Optional

from app.core.bedrock_client import bedrock_client
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


class GenerationRequest(BaseModel):
    context: str
    question: str
    model_id: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None


class GenerationResponse(BaseModel):
    answer: str
    model: str
    context_used: str
    question: str


@router.post("/generate", response_model=GenerationResponse)
async def generate_response(request: GenerationRequest):
    """
    Generate LLM response using AWS Bedrock.
    Decoupled from retrieval - expects context to be provided.
    
    Returns:
        Generated answer and metadata
    """
    try:
        # Construct prompt with explicit context boundaries
        prompt = f"""Context:
{request.context}

Question: {request.question}

Answer:"""
        
        # Override model if specified
        original_model = bedrock_client.model_id
        if request.model_id:
            bedrock_client.model_id = request.model_id
        
        try:
            # Generate response
            result = bedrock_client.generate(
                prompt=prompt,
                max_tokens=request.max_tokens,
                temperature=request.temperature
            )
            
            return JSONResponse({
                "answer": result["text"],
                "model": result["model"],
                "context_used": request.context[:200] + "..." if len(request.context) > 200 else request.context,
                "question": request.question
            })
            
        finally:
            # Restore original model
            bedrock_client.model_id = original_model
        
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")


@router.post("/rag")
async def rag_pipeline(request: GenerationRequest):
    """
    Combined RAG pipeline endpoint (retrieval + generation).
    For convenience - internally calls both layers.
    """
    try:
        # This endpoint combines retrieval and generation
        # In production, you might want to keep them separate
        # and call retrieval first, then generation
        
        prompt = f"""Context:
{request.context}

Question: {request.question}

Answer:"""
        
        result = bedrock_client.generate(
            prompt=prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        return JSONResponse({
            "answer": result["text"],
            "model": result["model"],
            "question": request.question
        })
        
    except Exception as e:
        logger.error(f"Error in RAG pipeline: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models")
async def list_models():
    """List available Bedrock models."""
    try:
        models = bedrock_client.list_available_models()
        return JSONResponse({"models": models})
    except Exception as e:
        logger.error(f"Error listing models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

