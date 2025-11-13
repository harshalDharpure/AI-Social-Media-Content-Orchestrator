"""
Service for generating social media content using LLM
"""
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from app.core.config import settings
from app.models.schemas import Platform, ContentRequest, ContentResponse, ContentStatus
from app.services.rag_service import RAGService
from typing import Optional, List
import logging
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)


class ContentGeneratorService:
    """Service for generating social media content"""
    
    def __init__(self):
        self.llm = None
        self.rag_service = RAGService()
    
    def _get_llm(self):
        """Get or initialize LLM"""
        if self.llm is None:
            self.llm = self._initialize_llm()
        return self.llm
    
    def _initialize_llm(self):
        """Initialize LLM based on available API keys"""
        if settings.ANTHROPIC_API_KEY:
            return ChatAnthropic(
                anthropic_api_key=settings.ANTHROPIC_API_KEY,
                model="claude-3-opus-20240229",
                temperature=0.7
            )
        elif settings.OPENAI_API_KEY:
            return ChatOpenAI(
                openai_api_key=settings.OPENAI_API_KEY,
                model_name="gpt-4",
                temperature=0.7
            )
        elif settings.GOOGLE_API_KEY:
            return ChatGoogleGenerativeAI(
                google_api_key=settings.GOOGLE_API_KEY,
                model="gemini-pro",
                temperature=0.7
            )
        else:
            raise ValueError("No LLM API key configured")
    
    def _get_platform_prompt(self, platform: Platform) -> str:
        """Get platform-specific prompt instructions"""
        prompts = {
            Platform.TWITTER: """
            Create a Twitter post that is:
            - Concise (under 280 characters)
            - Engaging with a strong hook
            - Uses relevant hashtags (2-3 max)
            - Includes a call-to-action when appropriate
            """,
            Platform.INSTAGRAM: """
            Create an Instagram post that is:
            - Visual and descriptive
            - Includes engaging caption (100-300 words)
            - Uses relevant hashtags (5-10)
            - Includes emojis for engagement
            - Has a strong opening line
            """,
            Platform.LINKEDIN: """
            Create a LinkedIn post that is:
            - Professional and informative
            - 100-300 words
            - Provides value to professionals
            - Uses relevant hashtags (3-5)
            - Includes a question or call-to-action
            """,
            Platform.FACEBOOK: """
            Create a Facebook post that is:
            - Conversational and engaging
            - 100-300 words
            - Includes relevant hashtags (2-4)
            - Encourages interaction
            """
        }
        return prompts.get(platform, prompts[Platform.TWITTER])
    
    async def generate_content(self, request: ContentRequest) -> ContentResponse:
        """Generate social media content"""
        try:
            # Get relevant context from RAG
            context = ""
            if request.brand_context:
                context = await self.rag_service.search(
                    query=request.topic,
                    top_k=3
                )
            
            # Build prompt
            system_prompt = f"""
            You are an expert social media content creator. 
            {self._get_platform_prompt(request.platform)}
            
            Brand context:
            {context if context else "No specific brand context provided."}
            
            Tone: {request.tone or "Professional and engaging"}
            """
            
            human_prompt = f"""
            Create a social media post about: {request.topic}
            
            Requirements:
            - Platform: {request.platform.value}
            - Length: {request.length or "Appropriate for the platform"}
            - Tone: {request.tone or "Professional and engaging"}
            """
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ]
            
            # Generate content
            llm = self._get_llm()
            response = llm.invoke(messages)
            content = response.content
            
            # Create response
            content_response = ContentResponse(
                id=str(uuid.uuid4()),
                content=content,
                platform=request.platform,
                status=ContentStatus.DRAFT,
                created_at=datetime.utcnow(),
                image_url=None
            )
            
            return content_response
        
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            raise
    
    async def generate_multiple_variations(self, request: ContentRequest, count: int = 3) -> List[ContentResponse]:
        """Generate multiple content variations"""
        variations = []
        for i in range(count):
            variation_request = ContentRequest(**request.dict())
            variation_request.topic = f"{request.topic} (variation {i+1})"
            variation = await self.generate_content(variation_request)
            variations.append(variation)
        return variations


# Global instance
content_generator = ContentGeneratorService()

