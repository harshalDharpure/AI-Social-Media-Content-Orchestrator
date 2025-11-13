"""
Scheduling router
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import PostRequest, PostResponse
from app.services.social_media import social_media_service
from app.core.scheduler import get_scheduler
from app.core.database import get_db
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
import logging
import uuid

logger = logging.getLogger(__name__)

router = APIRouter()


class SchedulePostRequest(PostRequest):
    """Schedule post request with content"""
    content: str


@router.post("/schedule", response_model=PostResponse)
async def schedule_post(request: SchedulePostRequest):
    """Schedule a post"""
    try:
        scheduler = get_scheduler()
        
        if request.schedule_for:
            # Schedule for future
            job_id = str(uuid.uuid4())
            scheduler.add_job(
                _publish_post,
                'date',
                run_date=request.schedule_for,
                args=[request, request.content],
                id=job_id
            )
            
            from app.models.schemas import ContentStatus
            return PostResponse(
                id=job_id,
                content_id=request.content_id,
                platform=request.platform,
                status=ContentStatus.SCHEDULED,
                scheduled_for=request.schedule_for
            )
        else:
            # Publish immediately
            post_request = PostRequest(
                content_id=request.content_id,
                platform=request.platform,
                image_url=request.image_url
            )
            return await _publish_post(post_request, request.content)
    except Exception as e:
        logger.error(f"Error scheduling post: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def _publish_post(request: PostRequest, content: str) -> PostResponse:
    """Publish a post"""
    try:
        response = await social_media_service.post(request, content)
        return response
    except Exception as e:
        logger.error(f"Error publishing post: {e}")
        raise


@router.get("/scheduled", response_model=List[PostResponse])
async def get_scheduled_posts():
    """Get scheduled posts"""
    try:
        scheduler = get_scheduler()
        jobs = scheduler.get_jobs()
        
        scheduled_posts = []
        for job in jobs:
            scheduled_posts.append({
                "id": job.id,
                "scheduled_for": job.next_run_time,
                "platform": job.args[0].platform if job.args else None
            })
        
        return scheduled_posts
    except Exception as e:
        logger.error(f"Error getting scheduled posts: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/scheduled/{post_id}")
async def cancel_scheduled_post(post_id: str):
    """Cancel a scheduled post"""
    try:
        scheduler = get_scheduler()
        scheduler.remove_job(post_id)
        return {"message": "Post cancelled successfully"}
    except Exception as e:
        logger.error(f"Error cancelling post: {e}")
        raise HTTPException(status_code=500, detail=str(e))

