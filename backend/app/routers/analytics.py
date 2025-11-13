"""
Analytics router
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import AnalyticsRequest, AnalyticsResponse
from app.services.analytics import analytics_service
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=AnalyticsResponse)
async def get_analytics(request: AnalyticsRequest):
    """Get analytics for a platform"""
    try:
        response = await analytics_service.get_analytics(request)
        return response
    except Exception as e:
        logger.error(f"Error getting analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/platform/{platform}")
async def get_platform_analytics(platform: str, days: int = 7):
    """Get analytics for a platform for the last N days"""
    try:
        from app.models.schemas import Platform
        
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        request = AnalyticsRequest(
            platform=Platform(platform),
            start_date=start_date,
            end_date=end_date
        )
        
        response = await analytics_service.get_analytics(request)
        return response
    except Exception as e:
        logger.error(f"Error getting platform analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

