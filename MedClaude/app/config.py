"""MedCore+ configuration — all env vars validated here."""
from pydantic_settings import BaseSettings
from typing import list


class Settings(BaseSettings):
    env: str = "development"
    model: str = "claude-opus-4-5"
    anthropic_api_key: str  # required, no default
    allowed_origins: list[str] = ["http://localhost:3000"]

    # RAG
    embedding_model: str = "text-embedding-3-large"
    retrieval_top_k: int = 10
    reranker_top_k: int = 3

    # Safety
    max_input_tokens: int = 8000
    pii_scan_enabled: bool = True
    output_filter_enabled: bool = True

    # Observability
    log_level: str = "INFO"
    cost_tracking_enabled: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
