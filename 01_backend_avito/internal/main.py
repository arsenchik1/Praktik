"""Main application entry point."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import endpoints
from .config.settings import get_settings
from .storage.database import init_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


def create_application() -> FastAPI:
    """Create FastAPI application."""
    settings = get_settings()
    
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        version="1.0.0",
        lifespan=lifespan
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(endpoints.router)
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy"}
    
    return app


app = create_application()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
