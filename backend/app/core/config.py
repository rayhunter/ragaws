"""
Application configuration settings.
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000"]
    
    # txtai Settings
    TXTAI_INDEX_PATH: str = "/mnt/efs/txtai_index"
    TXTAI_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 100
    
    # AWS Settings
    AWS_REGION: str = "us-east-1"
    AWS_S3_BUCKET: str = ""
    AWS_DYNAMODB_TABLE: str = "rag-metadata"
    
    # Bedrock Settings
    BEDROCK_MODEL_ID: str = "anthropic.claude-v2"  # Options: anthropic.claude-v2, amazon.titan-text-lite-v1, meta.llama2-13b-chat-v1
    BEDROCK_MAX_TOKENS: int = 2048
    BEDROCK_TEMPERATURE: float = 0.7
    
    # Retrieval Settings
    TOP_K_RESULTS: int = 5
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

