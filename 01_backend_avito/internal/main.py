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
    print("Starting up...")
    await init_db()
    print("Database initialized")
    yield
    # Shutdown
    print("Shutting down...")
    await close_db()
    print("Database closed")


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

    # Явно добавляем health check перед другими роутами
    @app.get("/health", tags=["health"])
    async def health_check():
        """Health check endpoint."""
        return {
            "status": "healthy",
            "database": "connected",
            "app": "running",
            "version": "1.0.0"
        }

    # Include routers
    app.include_router(endpoints.router)

    # Добавим корневой эндпоинт для проверки
    @app.get("/", tags=["root"])
    async def root():
        return {
            "message": "URL Shortener API",
            "docs": "/docs",
            "health": "/health"
        }

    return app


app = create_application()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
