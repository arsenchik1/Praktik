"""Configuration settings for the application."""
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    app_name: str = "URL Shortener"
    environment: str = "development"
    debug: bool = False
    base_url: str = "http://localhost:8000"
    
    # Database
    database_url: PostgresDsn
    database_pool_size: int = 20
    database_max_overflow: int = 10
    
    # Redis
    redis_url: Optional[str] = None
    cache_ttl: int = 3600
    
    # URL settings
    url_max_length: int = 2048
    short_id_length: int = 6
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings."""
    return Settings()
