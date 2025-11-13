"""
Content generation router
"""
from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import (
    ContentRequest,
    ContentResponse,
    BrainstormRequest,
    BrainstormResponse
)
from app.services.content_generator import content_generator
from app.services.brainstorming import brainstorming_service
from app.services.image_generator import image_generator
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/generate", response_model=ContentResponse)
async def generate_content(request: ContentRequest):
    """Generate social media content"""
    try:
        content = await content_generator.generate_content(request)
        
        # Generate image if requested
        if request.include_image:
            image_request = {
                "prompt": request.topic,
                "style": request.image_style,
                "width": 512,
                "height": 512,
                "num_images": 1
            }
            from app.models.schemas import ImageGenerationRequest
            image_req = ImageGenerationRequest(**image_request)
            image_response = await image_generator.generate_image(image_req)
            if image_response.image_urls:
                content.image_url = image_response.image_urls[0]
        
        return content
    except Exception as e:
        logger.error(f"Error generating content: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate/variations", response_model=List[ContentResponse])
async def generate_variations(request: ContentRequest, count: int = 3):
    """Generate multiple content variations"""
    try:
        variations = await content_generator.generate_multiple_variations(request, count)
        return variations
    except Exception as e:
        logger.error(f"Error generating variations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/brainstorm", response_model=BrainstormResponse)
async def brainstorm(request: BrainstormRequest):
    """Generate content ideas"""
    try:
        response = await brainstorming_service.brainstorm(request)
        return response
    except Exception as e:
        logger.error(f"Error brainstorming: {e}")
        raise HTTPException(status_code=500, detail=str(e))

