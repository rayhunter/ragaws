"""
txtai embeddings client for semantic search.
"""
from txtai.embeddings import Embeddings
import os
import logging
from typing import List, Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)


class TxtaiClient:
    """Singleton txtai embeddings client."""
    
    _instance = None
    _embeddings = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TxtaiClient, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._embeddings is None:
            self._initialize_embeddings()
    
    def _initialize_embeddings(self):
        """Initialize txtai embeddings with persistent storage."""
        try:
            index_path = settings.TXTAI_INDEX_PATH
            
            # Ensure directory exists
            os.makedirs(index_path, exist_ok=True)
            
            # Initialize embeddings
            self._embeddings = Embeddings({
                "path": settings.TXTAI_MODEL,
                "content": True,
                "backend": "faiss"
            })
            
            # Load existing index if available
            index_file = os.path.join(index_path, "index")
            if os.path.exists(index_file):
                self._embeddings.load(index_file)
                logger.info(f"Loaded existing index from {index_file}")
            else:
                logger.info("Initializing new embeddings index")
                
        except Exception as e:
            logger.error(f"Error initializing txtai embeddings: {e}")
            raise
    
    def index_documents(self, documents: List[Dict[str, Any]]) -> int:
        """
        Index documents with metadata.
        
        Args:
            documents: List of dicts with 'id', 'text', and optional 'metadata'
        
        Returns:
            Number of documents indexed
        """
        try:
            # Format for txtai: (id, text, metadata)
            formatted = [
                (doc["id"], doc["text"], doc.get("metadata", None))
                for doc in documents
            ]
            
            self._embeddings.index(formatted)
            self._save_index()
            
            logger.info(f"Indexed {len(documents)} documents")
            return len(documents)
            
        except Exception as e:
            logger.error(f"Error indexing documents: {e}")
            raise
    
    def search(self, query: str, limit: int = None) -> List[Dict[str, Any]]:
        """
        Semantic search for relevant documents.
        
        Args:
            query: Search query string
            limit: Maximum number of results (defaults to TOP_K_RESULTS)
        
        Returns:
            List of relevant documents with scores
        """
        try:
            limit = limit or settings.TOP_K_RESULTS
            
            results = self._embeddings.search(query, limit)
            
            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "id": result["id"],
                    "text": result["text"],
                    "score": result.get("score", 0.0),
                    "metadata": result.get("metadata", {})
                })
            
            logger.info(f"Search returned {len(formatted_results)} results for query: {query[:50]}")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error during search: {e}")
            raise
    
    def _save_index(self):
        """Save embeddings index to persistent storage."""
        try:
            index_path = settings.TXTAI_INDEX_PATH
            index_file = os.path.join(index_path, "index")
            self._embeddings.save(index_file)
            logger.debug(f"Saved index to {index_file}")
        except Exception as e:
            logger.error(f"Error saving index: {e}")
            raise
    
    def get_stats(self) -> Dict[str, Any]:
        """Get index statistics."""
        try:
            count = len(self._embeddings) if hasattr(self._embeddings, '__len__') else 0
            return {
                "total_documents": count,
                "model": settings.TXTAI_MODEL,
                "index_path": settings.TXTAI_INDEX_PATH
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {"error": str(e)}


# Global singleton instance
txtai_client = TxtaiClient()

