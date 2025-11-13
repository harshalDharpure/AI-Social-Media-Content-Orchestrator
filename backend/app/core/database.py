"""
Database initialization and connection
"""
from supabase import create_client, Client
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Global Supabase client
supabase: Client = None


async def init_db():
    """Initialize database connection"""
    global supabase
    try:
        if settings.SUPABASE_URL and settings.SUPABASE_KEY:
            supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
            logger.info("Database connection established")
        else:
            logger.warning("Supabase credentials not provided. Using in-memory storage.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


def get_db() -> Client:
    """Get database client"""
    if supabase is None:
        raise Exception("Database not initialized")
    return supabase

