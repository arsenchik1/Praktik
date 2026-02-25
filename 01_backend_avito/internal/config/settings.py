"""Configuration settings for the application."""
from functools import lru_cache
from typing import Optional, Any
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, field_validator
from pydantic_core import Url


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    app_name: str = "URL Shortener"
    environment: str = "development"
    debug: bool = False
    base_url: str = "http://localhost:8000"
    
    # Database - можно использовать любой URL
    database_url: str = "sqlite+aiosqlite:///./urls.db"
    database_pool_size: int = 20
    database_max_overflow: int = 10
    
    # Redis
    redis_url: Optional[str] = None
    cache_ttl: int = 3600
    
    # URL settings
    url_max_length: int = 2048
    short_id_length: int = 6
    
    @field_validator('database_url', mode='before')
    @classmethod
    def validate_database_url(cls, v: Any) -> str:
        """Allow any database URL, not just PostgreSQL."""
        if v is None:
            return "sqlite+aiosqlite:///./urls.db"
        return str(v)
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings."""
    return Settings()
