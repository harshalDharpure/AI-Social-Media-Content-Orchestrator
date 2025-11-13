"""
Service for image generation using Stable Diffusion
"""
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import io
import base64
import httpx
from app.core.config import settings
from app.models.schemas import ImageGenerationRequest, ImageGenerationResponse
from typing import List
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)


class ImageGeneratorService:
    """Service for generating images"""
    
    def __init__(self):
        self.pipeline = None
        self.use_api = False
        self.api_url = settings.STABLE_DIFFUSION_API_URL
    
    def _initialize_pipeline(self):
        """Initialize Stable Diffusion pipeline"""
        try:
            if torch.cuda.is_available():
                device = "cuda"
                dtype = torch.float16
            else:
                device = "cpu"
                dtype = torch.float32
            
            self.pipeline = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                torch_dtype=dtype
            )
            self.pipeline = self.pipeline.to(device)
            logger.info(f"Stable Diffusion pipeline initialized on {device}")
        except Exception as e:
            logger.error(f"Error initializing pipeline: {e}")
            logger.info("Falling back to API-based generation")
            self.use_api = True
    
    async def generate_image(self, request: ImageGenerationRequest) -> ImageGenerationResponse:
        """Generate image from prompt"""
        try:
            if self.use_api or self.api_url:
                return await self._generate_via_api(request)
            else:
                return await self._generate_locally(request)
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            raise
    
    async def _generate_via_api(self, request: ImageGenerationRequest) -> ImageGenerationResponse:
        """Generate image via API"""
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                payload = {
                    "prompt": request.prompt,
                    "negative_prompt": request.negative_prompt or "",
                    "width": request.width,
                    "height": request.height,
                    "num_images": request.num_images,
                    "steps": 50,
                    "guidance_scale": 7.5
                }
                
                response = await client.post(
                    f"{self.api_url}/api/v1/generate",
                    json=payload
                )
                response.raise_for_status()
                
                result = response.json()
                image_urls = result.get("images", [])
                
                return ImageGenerationResponse(
                    image_urls=image_urls,
                    prompt=request.prompt,
                    metadata={
                        "width": request.width,
                        "height": request.height,
                        "generated_at": datetime.utcnow().isoformat()
                    }
                )
        except Exception as e:
            logger.error(f"Error generating image via API: {e}")
            # Fallback to local generation if API fails
            if not self.use_api:
                return await self._generate_locally(request)
            raise
    
    async def _generate_locally(self, request: ImageGenerationRequest) -> ImageGenerationResponse:
        """Generate image locally"""
        try:
            if self.pipeline is None:
                self._initialize_pipeline()
            
            if self.pipeline is None:
                raise Exception("Pipeline not initialized and API not available")
            
            images = []
            for _ in range(request.num_images):
                image = self.pipeline(
                    prompt=request.prompt,
                    negative_prompt=request.negative_prompt,
                    width=request.width,
                    height=request.height,
                    num_inference_steps=50,
                    guidance_scale=7.5
                ).images[0]
                
                # Save image and get URL
                image_url = await self._save_image(image)
                images.append(image_url)
            
            return ImageGenerationResponse(
                image_urls=images,
                prompt=request.prompt,
                metadata={
                    "width": request.width,
                    "height": request.height,
                    "generated_at": datetime.utcnow().isoformat(),
                    "method": "local"
                }
            )
        except Exception as e:
            logger.error(f"Error generating image locally: {e}")
            raise
    
    async def _save_image(self, image: Image.Image) -> str:
        """Save image and return URL"""
        try:
            # Create uploads directory if it doesn't exist
            os.makedirs("uploads/images", exist_ok=True)
            
            # Generate filename
            filename = f"image_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = f"uploads/images/{filename}"
            
            # Save image
            image.save(filepath)
            
            # Return URL (in production, this would be uploaded to cloud storage)
            return f"/uploads/images/{filename}"
        except Exception as e:
            logger.error(f"Error saving image: {e}")
            raise


# Global instance
image_generator = ImageGeneratorService()

