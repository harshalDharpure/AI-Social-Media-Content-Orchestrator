"""
Pydantic schemas for API requests and responses
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class Platform(str, Enum):
    """Social media platforms"""
    TWITTER = "twitter"
    INSTAGRAM = "instagram"
    LINKEDIN = "linkedin"
    FACEBOOK = "facebook"


class ContentStatus(str, Enum):
    """Content status"""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"


class ContentRequest(BaseModel):
    """Request to generate content"""
    topic: str = Field(..., description="Topic for content generation")
    platform: Platform = Field(..., description="Target platform")
    tone: Optional[str] = Field(None, description="Content tone")
    length: Optional[int] = Field(None, description="Content length in characters")
    include_image: bool = Field(False, description="Whether to generate image")
    image_style: Optional[str] = Field(None, description="Image style")
    brand_context: Optional[str] = Field(None, description="Brand context")


class ContentResponse(BaseModel):
    """Generated content response"""
    id: str
    content: str
    image_url: Optional[str] = None
    platform: Platform
    status: ContentStatus
    created_at: datetime
    scheduled_for: Optional[datetime] = None


class PostRequest(BaseModel):
    """Request to publish content"""
    content_id: str
    platform: Platform
    schedule_for: Optional[datetime] = None
    image_url: Optional[str] = None


class PostResponse(BaseModel):
    """Post response"""
    id: str
    content_id: str = ""
    platform: Platform
    status: ContentStatus
    post_url: Optional[str] = None
    published_at: Optional[datetime] = None
    scheduled_for: Optional[datetime] = None
    error: Optional[str] = None


class TrendingTopic(BaseModel):
    """Trending topic"""
    keyword: str
    trend_score: float
    platform: str
    source: str


class BrainstormRequest(BaseModel):
    """Request for content brainstorming"""
    topics: Optional[List[str]] = None
    platform: Platform
    count: int = Field(5, ge=1, le=20)


class BrainstormResponse(BaseModel):
    """Brainstorming response"""
    ideas: List[Dict[str, Any]]
    trending_topics: List[TrendingTopic]


class RAGDocument(BaseModel):
    """RAG document"""
    id: str
    content: str
    metadata: Dict[str, Any]
    created_at: datetime


class RAGUploadRequest(BaseModel):
    """Request to upload document to RAG"""
    content: str
    metadata: Optional[Dict[str, Any]] = None
    document_type: Optional[str] = None


class AnalyticsRequest(BaseModel):
    """Request for analytics"""
    platform: Platform
    start_date: datetime
    end_date: datetime
    metrics: Optional[List[str]] = None


class AnalyticsResponse(BaseModel):
    """Analytics response"""
    platform: Platform
    metrics: Dict[str, Any]
    recommendations: List[str]
    period: Dict[str, datetime]


class ImageGenerationRequest(BaseModel):
    """Request to generate image"""
    prompt: str
    style: Optional[str] = None
    negative_prompt: Optional[str] = None
    width: int = Field(512, ge=256, le=1024)
    height: int = Field(512, ge=256, le=1024)
    num_images: int = Field(1, ge=1, le=4)


class ImageGenerationResponse(BaseModel):
    """Image generation response"""
    image_urls: List[str]
    prompt: str
    metadata: Dict[str, Any]

