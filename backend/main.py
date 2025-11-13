"""
AI Social Media Content Orchestrator - FastAPI Backend
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager
import uvicorn
import logging

from app.routers import (
    content,
    scheduling,
    analytics,
    social_media,
    images,
    rag,
    auth
)
from app.core.config import settings
from app.core.database import init_db
from app.core.scheduler import init_scheduler
from app.core.logging_config import setup_logging
from app.core.middleware import LoggingMiddleware, SecurityHeadersMiddleware
from app.core.rate_limit import RateLimitMiddleware
from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("Starting up...")
    try:
        await init_db()
        init_scheduler()
        logger.info("Application started successfully!")
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")


# Initialize FastAPI app
app = FastAPI(
    title="AI Social Media Content Orchestrator",
    description="End-to-end automation for social media content creation and scheduling",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
)

# Add custom middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

# Rate limiting (disabled in development for easier testing)
if settings.ENVIRONMENT == "production":
    app.add_middleware(RateLimitMiddleware, calls=100, period=60)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(content.router, prefix="/api/content", tags=["Content"])
app.include_router(scheduling.router, prefix="/api/scheduling", tags=["Scheduling"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(social_media.router, prefix="/api/social-media", tags=["Social Media"])
app.include_router(images.router, prefix="/api/images", tags=["Images"])
app.include_router(rag.router, prefix="/api/rag", tags=["RAG"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Social Media Content Orchestrator API",
        "version": "1.0.0",
        "docs": "/docs" if settings.ENVIRONMENT != "production" else "Disabled in production",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        db_status = "healthy"
        try:
            from app.core.database import get_db
            get_db()
        except:
            db_status = "unhealthy"
        
        return {
            "status": "healthy" if db_status == "healthy" else "degraded",
            "database": db_status,
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development"
    )
