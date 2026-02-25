"""Tests for API endpoints."""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from ..internal.main import app
from ..internal.models.url import Base
from ..internal.storage.database import get_db

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/test_db"

# Create test engine
test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestAsyncSessionLocal = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


async def override_get_db():
    """Override database dependency for testing."""
    async with TestAsyncSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
async def setup_database():
    """Setup test database before each test."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_create_short_url():
    """Test creating short URL."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/shorten",
            json={"url": "https://example.com"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "short_url" in data
        assert data["original_url"] == "https://example.com"
        assert data["custom"] is False


@pytest.mark.asyncio
async def test_create_custom_url():
    """Test creating custom short URL."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/shorten",
            json={
                "url": "https://example.com",
                "custom_id": "mycustom"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["short_id"] == "mycustom"
        assert data["custom"] is True


@pytest.mark.asyncio
async def test_duplicate_custom_url():
    """Test creating duplicate custom URL."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create first
        await client.post(
            "/shorten",
            json={
                "url": "https://example.com",
                "custom_id": "duplicate"
            }
        )
        
        # Try to create duplicate
        response = await client.post(
            "/shorten",
            json={
                "url": "https://another.com",
                "custom_id": "duplicate"
            }
        )
        
        assert response.status_code == 400
        assert "already taken" in response.json()["detail"]


@pytest.mark.asyncio
async def test_invalid_url():
    """Test invalid URL validation."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/shorten",
            json={"url": "not-a-valid-url"}
        )
        
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_redirect():
    """Test URL redirection."""
    async with AsyncClient(app=app, base_url="http://test", follow_redirects=False) as client:
        # Create URL
        create_response = await client.post(
            "/shorten",
            json={"url": "https://example.com"}
        )
        data = create_response.json()
        short_id = data["short_id"]
        
        # Test redirect
        response = await client.get(f"/{short_id}")
        assert response.status_code == 302
        assert response.headers["location"] == "https://example.com"


@pytest.mark.asyncio
async def test_stats():
    """Test URL statistics."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create URL
        create_response = await client.post(
            "/shorten",
            json={"url": "https://example.com"}
        )
        data = create_response.json()
        short_id = data["short_id"]
        
        # Get stats
        response = await client.get(f"/stats/{short_id}")
        assert response.status_code == 200
        stats = response.json()
        assert stats["short_id"] == short_id
        assert stats["clicks"] == 0


@pytest.mark.asyncio
async def test_delete():
    """Test URL deletion."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create URL
        create_response = await client.post(
            "/shorten",
            json={"url": "https://example.com"}
        )
        data = create_response.json()
        short_id = data["short_id"]
        
        # Delete URL
        delete_response = await client.delete(f"/{short_id}")
        assert delete_response.status_code == 200
        
        # Try to get deleted URL
        get_response = await client.get(f"/{short_id}")
        assert get_response.status_code == 404
