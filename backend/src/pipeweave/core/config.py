"""Configuration Settings"""
import os
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List

class Settings(BaseSettings):
    app_env: str = Field(default="development", alias="PIPEWEAVE_ENV")
    app_name: str = Field(default="PipeWeave Platform", alias="PIPEWEAVE_APP_NAME")
    api_host: str = Field(default="0.0.0.0", alias="PIPEWEAVE_HOST")
    api_port: int = Field(default=8000, alias="PIPEWEAVE_PORT")
    debug: bool = Field(default=True, alias="PIPEWEAVE_DEBUG")
    secret_key: str = Field(default="pipeweave-secret-key-2026", alias="PIPEWEAVE_SECRET_KEY")
    database_url: str = Field(default="sqlite+aiosqlite:///./pipeweave.db", alias="PIPEWEAVE_DATABASE_URL")
    storage_path: str = Field(default="./data/storage", alias="PIPEWEAVE_STORAGE_PATH")
    worker_concurrency: int = Field(default=16, alias="PIPEWEAVE_WORKER_CONCURRENCY")
    cors_origins: List[str] = ["*"]

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
os.makedirs(settings.storage_path, exist_ok=True)
