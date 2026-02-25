"""URL models for database and API."""
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, DateTime, Integer, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, field_validator

Base = declarative_base()


class URLDB(Base):
    """URL database model."""
    
    __tablename__ = "urls"
    
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String(2048), nullable=False)
    short_id = Column(String(50), unique=True, index=True, nullable=False)
    custom = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    clicks = Column(Integer, default=0)
    
    __table_args__ = (
        Index('idx_short_id', 'short_id'),
        Index('idx_created_at', 'created_at'),
    )


class URLCreate(BaseModel):
    """URL creation request model."""
    
    url: str
    custom_id: Optional[str] = None
    
    @field_validator('url')
    def validate_url(cls, v):
        """Validate URL format."""
        import validators
        if not validators.url(v):
            raise ValueError('Invalid URL format')
        return v
    
    @field_validator('custom_id')
    def validate_custom_id(cls, v):
        """Validate custom ID format."""
        if v:
            if not v.isalnum() or len(v) < 3 or len(v) > 50:
                raise ValueError('Custom ID must be alphanumeric and 3-50 characters')
        return v


class URLResponse(BaseModel):
    """URL creation response model."""
    
    short_url: str
    original_url: str
    short_id: str
    custom: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class URLStats(BaseModel):
    """URL statistics response model."""
    
    short_id: str
    original_url: str
    clicks: int
    created_at: datetime
    
    class Config:
        from_attributes = True
