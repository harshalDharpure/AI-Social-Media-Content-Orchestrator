"""
Social media router
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import PostRequest, PostResponse
from app.services.social_media import social_media_service
from app.core.config import settings
from pydantic import BaseModel
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class PostContentRequest(PostRequest):
    """Post content request with content"""
    content: str


@router.post("/post", response_model=PostResponse)
async def post_content(request: PostContentRequest):
    """Post content to social media"""
    try:
        post_request = PostRequest(
            content_id=request.content_id,
            platform=request.platform,
            image_url=request.image_url
        )
        response = await social_media_service.post(post_request, request.content)
        return response
    except Exception as e:
        logger.error(f"Error posting to social media: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/platforms")
async def get_platforms():
    """Get available platforms"""
    return {
        "platforms": [
            {
                "name": "twitter",
                "enabled": social_media_service.twitter_api is not None,
                "features": ["text", "image"]
            },
            {
                "name": "instagram",
                "enabled": bool(settings.INSTAGRAM_ACCESS_TOKEN and settings.INSTAGRAM_APP_ID),
                "features": ["image", "caption"]
            },
            {
                "name": "linkedin",
                "enabled": social_media_service.linkedin_enabled,
                "features": ["text", "image"]
            }
        ]
    }

