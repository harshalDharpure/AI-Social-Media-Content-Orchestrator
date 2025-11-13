"""
Service for content brainstorming using LLM and trending topics
"""
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from app.core.config import settings
from app.models.schemas import BrainstormRequest, BrainstormResponse, Platform, TrendingTopic
from app.services.trending_topics import trending_service
from app.services.content_generator import content_generator
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class BrainstormingService:
    """Service for content brainstorming"""
    
    def __init__(self):
        self.llm = None
    
    def _get_llm(self):
        """Get or initialize LLM"""
        if self.llm is None:
            self.llm = self._initialize_llm()
        return self.llm
    
    def _initialize_llm(self):
        """Initialize LLM"""
        if settings.ANTHROPIC_API_KEY:
            return ChatAnthropic(
                anthropic_api_key=settings.ANTHROPIC_API_KEY,
                model="claude-3-opus-20240229",
                temperature=0.9
            )
        elif settings.OPENAI_API_KEY:
            return ChatOpenAI(
                openai_api_key=settings.OPENAI_API_KEY,
                model_name="gpt-4",
                temperature=0.9
            )
        elif settings.GOOGLE_API_KEY:
            return ChatGoogleGenerativeAI(
                google_api_key=settings.GOOGLE_API_KEY,
                model="gemini-pro",
                temperature=0.9
            )
        else:
            raise ValueError("No LLM API key configured")
    
    async def brainstorm(self, request: BrainstormRequest) -> BrainstormResponse:
        """Generate content ideas"""
        try:
            # Get trending topics
            trending_topics = await trending_service.get_all_trending()
            
            # Filter by platform if needed
            if request.topics:
                trending_topics = [t for t in trending_topics if t.keyword in request.topics]
            
            # Generate content ideas using LLM
            ideas = await self._generate_ideas(request, trending_topics)
            
            return BrainstormResponse(
                ideas=ideas,
                trending_topics=trending_topics[:10]  # Top 10 trending topics
            )
        except Exception as e:
            logger.error(f"Error brainstorming: {e}")
            raise
    
    async def _generate_ideas(self, request: BrainstormRequest, trending_topics: List[TrendingTopic]) -> List[Dict[str, Any]]:
        """Generate content ideas using LLM"""
        try:
            # Build prompt with trending topics
            topics_text = "\n".join([f"- {t.keyword} (score: {t.trend_score})" for t in trending_topics[:20]])
            
            system_prompt = f"""
            You are an expert social media content strategist. Generate creative and engaging content ideas
            for {request.platform.value} platform.
            
            Trending topics:
            {topics_text}
            
            Generate {request.count} unique content ideas with:
            1. A compelling hook
            2. Key talking points
            3. Suggested hashtags
            4. Engagement strategy
            """
            
            human_prompt = f"""
            Generate {request.count} creative content ideas for {request.platform.value} platform.
            Each idea should be unique, engaging, and leverage trending topics when relevant.
            
            Format each idea as JSON with:
            - title: Brief title for the idea
            - hook: Compelling opening hook
            - key_points: List of 3-5 key points
            - hashtags: List of 5-10 relevant hashtags
            - engagement_strategy: How to encourage engagement
            - trending_relevance: How it relates to trending topics
            """
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=human_prompt)
            ]
            
            # Generate ideas
            llm = self._get_llm()
            response = llm.invoke(messages)
            content = response.content
            
            # Parse response (simplified - in production, use structured output)
            ideas = self._parse_ideas(content, request.count)
            
            return ideas
        except Exception as e:
            logger.error(f"Error generating ideas: {e}")
            return []
    
    def _parse_ideas(self, content: str, count: int) -> List[Dict[str, Any]]:
        """Parse LLM response into structured ideas"""
        # Simplified parser - in production, use structured output or JSON parsing
        ideas = []
        lines = content.split("\n")
        
        current_idea = {}
        for line in lines:
            if "title" in line.lower() or "idea" in line.lower():
                if current_idea:
                    ideas.append(current_idea)
                    current_idea = {}
                # Extract title
                title = line.split(":")[-1].strip() if ":" in line else line.strip()
                current_idea["title"] = title
            elif "hook" in line.lower():
                hook = line.split(":")[-1].strip() if ":" in line else line.strip()
                current_idea["hook"] = hook
            elif "hashtag" in line.lower():
                hashtags = [h.strip() for h in line.split(":")[-1].split(",") if h.strip()]
                current_idea["hashtags"] = hashtags
        
        if current_idea:
            ideas.append(current_idea)
        
        # If parsing failed, create default ideas
        if len(ideas) < count:
            for i in range(len(ideas), count):
                ideas.append({
                    "title": f"Content Idea {i+1}",
                    "hook": "Engaging hook for your audience",
                    "key_points": ["Point 1", "Point 2", "Point 3"],
                    "hashtags": ["#trending", "#social", "#content"],
                    "engagement_strategy": "Ask questions and encourage comments",
                    "trending_relevance": "Relates to current trends"
                })
        
        return ideas[:count]


# Global instance
brainstorming_service = BrainstormingService()

