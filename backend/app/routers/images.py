"""
Image generation router
"""
from fastapi import APIRouter, HTTPException
from app.models.schemas import ImageGenerationRequest, ImageGenerationResponse
from app.services.image_generator import image_generator
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/generate", response_model=ImageGenerationResponse)
async def generate_image(request: ImageGenerationRequest):
    """Generate image from prompt"""
    try:
        response = await image_generator.generate_image(request)
        return response
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze")
async def analyze_image(image_url: str):
    """Analyze image for insights"""
    try:
        # Placeholder for image analysis
        # In production, use vision models to analyze images
        return {
            "image_url": image_url,
            "insights": {
                "aesthetics": "high",
                "tone": "professional",
                "colors": ["blue", "white"],
                "engagement_potential": "high"
            }
        }
    except Exception as e:
        logger.error(f"Error analyzing image: {e}")
        raise HTTPException(status_code=500, detail=str(e))

