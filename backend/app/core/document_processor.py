"""
Document processing utilities for PDF and Markdown files.
"""
import fitz  # PyMuPDF
import markdown2
import logging
from typing import List, Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Process documents and chunk text."""
    
    @staticmethod
    def process_pdf(file_content: bytes, filename: str) -> str:
        """
        Extract text from PDF file.
        
        Args:
            file_content: PDF file bytes
            filename: Original filename
        
        Returns:
            Extracted text
        """
        try:
            doc = fitz.open(stream=file_content, filetype="pdf")
            text_parts = []
            
            for page_num, page in enumerate(doc):
                text = page.get_text()
                text_parts.append(text)
            
            doc.close()
            full_text = "\n\n".join(text_parts)
            
            logger.info(f"Extracted {len(full_text)} characters from PDF: {filename}")
            return full_text
            
        except Exception as e:
            logger.error(f"Error processing PDF {filename}: {e}")
            raise
    
    @staticmethod
    def process_markdown(file_content: bytes, filename: str) -> str:
        """
        Extract text from Markdown file.
        
        Args:
            file_content: Markdown file bytes
            filename: Original filename
        
        Returns:
            Extracted text (HTML converted to plain text)
        """
        try:
            md_text = file_content.decode('utf-8')
            # Convert markdown to HTML, then extract text
            html = markdown2.markdown(md_text)
            
            # Simple HTML to text conversion
            import re
            text = re.sub(r'<[^>]+>', '', html)
            
            logger.info(f"Extracted {len(text)} characters from Markdown: {filename}")
            return text
            
        except Exception as e:
            logger.error(f"Error processing Markdown {filename}: {e}")
            raise
    
    @staticmethod
    def chunk_text(
        text: str,
        chunk_size: int = None,
        overlap: int = None
    ) -> List[Dict[str, Any]]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Input text
            chunk_size: Size of each chunk in characters
            overlap: Overlap between chunks in characters
        
        Returns:
            List of chunk dictionaries with id, text, and metadata
        """
        chunk_size = chunk_size or settings.CHUNK_SIZE
        overlap = overlap or settings.CHUNK_OVERLAP
        
        chunks = []
        start = 0
        chunk_id = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]
            
            chunks.append({
                "id": f"chunk_{chunk_id}",
                "text": chunk_text,
                "metadata": {
                    "start": start,
                    "end": end,
                    "chunk_index": chunk_id
                }
            })
            
            start = end - overlap
            chunk_id += 1
        
        logger.info(f"Created {len(chunks)} chunks from text")
        return chunks


document_processor = DocumentProcessor()

