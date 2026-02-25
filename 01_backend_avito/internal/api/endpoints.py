"""API endpoints for URL shortener."""
from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import random
import string

from ..models.url import URLDB, URLCreate, URLResponse, URLStats
from ..storage.database import get_db
from ..config.settings import get_settings

router = APIRouter()


def generate_short_id(length: int = 6) -> str:
    """Generate random short ID."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choices(alphabet, k=length))


@router.post("/shorten", response_model=URLResponse)
async def create_short_url(
    url_data: URLCreate,
    db: AsyncSession = Depends(get_db),
    settings = Depends(get_settings)
):
    """Create short URL from original URL."""
    short_id = url_data.custom_id
    
    if url_data.custom_id:
        # Check if custom ID already exists
        result = await db.execute(
            select(URLDB).where(URLDB.short_id == url_data.custom_id)
        )
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(status_code=400, detail="Custom ID already taken")
    else:
        # Generate unique short ID
        while True:
            short_id = generate_short_id(settings.short_id_length)
            result = await db.execute(
                select(URLDB).where(URLDB.short_id == short_id)
            )
            existing = result.scalar_one_or_none()
            if not existing:
                break
    
    # Create new URL entry
    db_url = URLDB(
        original_url=url_data.url,
        short_id=short_id,
        custom=bool(url_data.custom_id)
    )
    
    db.add(db_url)
    await db.commit()
    await db.refresh(db_url)
    
    return URLResponse(
        short_url=f"{settings.base_url}/{short_id}",
        original_url=db_url.original_url,
        short_id=db_url.short_id,
        custom=db_url.custom,
        created_at=db_url.created_at
    )


@router.get("/{short_id}")
async def redirect_to_url(
    short_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Redirect to original URL."""
    result = await db.execute(
        select(URLDB).where(URLDB.short_id == short_id)
    )
    url_entry = result.scalar_one_or_none()
    
    if not url_entry:
        raise HTTPException(status_code=404, detail="URL not found")
    
    # Increment click count
    url_entry.clicks += 1
    await db.commit()
    
    return Response(
        status_code=302,
        headers={"Location": url_entry.original_url}
    )


@router.get("/stats/{short_id}", response_model=URLStats)
async def get_url_stats(
    short_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get statistics for a short URL."""
    result = await db.execute(
        select(URLDB).where(URLDB.short_id == short_id)
    )
    url_entry = result.scalar_one_or_none()
    
    if not url_entry:
        raise HTTPException(status_code=404, detail="URL not found")
    
    return URLStats(
        short_id=url_entry.short_id,
        original_url=url_entry.original_url,
        clicks=url_entry.clicks,
        created_at=url_entry.created_at
    )


@router.delete("/{short_id}")
async def delete_short_url(
    short_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Delete a short URL."""
    result = await db.execute(
        select(URLDB).where(URLDB.short_id == short_id)
    )
    url_entry = result.scalar_one_or_none()
    
    if not url_entry:
        raise HTTPException(status_code=404, detail="URL not found")
    
    await db.delete(url_entry)
    await db.commit()
    
    return {"message": "URL deleted successfully"}
