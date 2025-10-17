"""Application configuration using Pydantic settings."""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings."""

    # Application
    APP_NAME: str = "JobRight Clone"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql://jobright:jobright_password@localhost:5432/jobright_db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Vector Database
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION_NAME: str = "job_embeddings"
    EMBEDDING_SIZE: int = 384  # all-MiniLM-L6-v2 dimension

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # AI APIs / LLM Configuration
    LLM_PROVIDER: str = "ollama"  # "ollama" (FREE!), "anthropic", or "openai"
    OLLAMA_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.1"  # Easy to change! Try: llama3.1, mistral, codellama, phi3

    # Optional: Cloud API keys (if you want to use them instead)
    ANTHROPIC_API_KEY: str = ""
    OPENAI_API_KEY: str = ""

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:80"]

    # Job Scraping
    JOBS_SCRAPE_INTERVAL_HOURS: int = 6
    MAX_JOBS_PER_SCRAPE: int = 100

    # ML Models
    SENTENCE_TRANSFORMER_MODEL: str = "all-MiniLM-L6-v2"

    # File Upload
    UPLOAD_DIR: str = "/app/uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
