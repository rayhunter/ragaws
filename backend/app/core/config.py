"""
Application configuration settings.
"""
import json
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: List[str] = Field(
        default_factory=lambda: ["http://localhost:5173", "http://localhost:3000"]
    )
    
    # txtai Settings
    TXTAI_INDEX_PATH: str = "./data/txtai_index"  # Use local path by default, override with env var for AWS EFS
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

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, value):
        """
        Allow environment variables to provide CORS origins as a JSON array or
        comma-separated string.
        """
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            value = value.strip()
            if not value:
                return []
            if value.startswith("[") and value.endswith("]"):
                try:
                    parsed = json.loads(value)
                    if isinstance(parsed, list):
                        return parsed
                except json.JSONDecodeError as exc:
                    raise ValueError("Invalid JSON for CORS_ORIGINS") from exc
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
