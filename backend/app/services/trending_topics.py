"""
Service for fetching trending topics from various sources
"""
from pytrends.request import TrendReq
import praw
import tweepy
from app.core.config import settings
from app.models.schemas import TrendingTopic
from typing import List
import logging
import feedparser
import httpx

logger = logging.getLogger(__name__)


class TrendingTopicsService:
    """Service for fetching trending topics"""
    
    def __init__(self):
        self.pytrends = TrendReq(hl='en-US', tz=360)
        
        # Initialize Reddit client
        if settings.REDDIT_CLIENT_ID and settings.REDDIT_CLIENT_SECRET:
            self.reddit = praw.Reddit(
                client_id=settings.REDDIT_CLIENT_ID,
                client_secret=settings.REDDIT_CLIENT_SECRET,
                user_agent=settings.REDDIT_USER_AGENT or "SocialMediaBot/1.0"
            )
        else:
            self.reddit = None
        
        # Initialize Twitter client
        if settings.TWITTER_BEARER_TOKEN:
            self.twitter_client = tweepy.Client(
                bearer_token=settings.TWITTER_BEARER_TOKEN
            )
        else:
            self.twitter_client = None
    
    async def get_google_trends(self, keywords: List[str] = None, geo: str = "US") -> List[TrendingTopic]:
        """Get trending topics from Google Trends"""
        try:
            if keywords:
                self.pytrends.build_payload(keywords, cat=0, timeframe='today 3-m', geo=geo)
                data = self.pytrends.interest_over_time()
                trends = []
                for keyword in keywords:
                    if keyword in data.columns:
                        score = data[keyword].mean()
                        trends.append(TrendingTopic(
                            keyword=keyword,
                            trend_score=float(score),
                            platform="google",
                            source="google_trends"
                        ))
                return trends
            else:
                # Get trending searches
                trending = self.pytrends.trending_searches(pn='united_states')
                trends = []
                for idx, keyword in enumerate(trending[0].head(10)):
                    trends.append(TrendingTopic(
                        keyword=str(keyword),
                        trend_score=10 - idx,
                        platform="google",
                        source="google_trends"
                    ))
                return trends
        except Exception as e:
            logger.error(f"Error fetching Google Trends: {e}")
            return []
    
    async def get_reddit_trending(self, subreddit: str = "all", limit: int = 10) -> List[TrendingTopic]:
        """Get trending topics from Reddit"""
        if not self.reddit:
            logger.warning("Reddit client not configured")
            return []
        
        try:
            subreddit_obj = self.reddit.subreddit(subreddit)
            trends = []
            for idx, post in enumerate(subreddit_obj.hot(limit=limit)):
                score = post.score
                trends.append(TrendingTopic(
                    keyword=post.title,
                    trend_score=float(score),
                    platform="reddit",
                    source=f"r/{subreddit}"
                ))
            return trends
        except Exception as e:
            logger.error(f"Error fetching Reddit trends: {e}")
            return []
    
    async def get_twitter_trending(self, location: str = "1") -> List[TrendingTopic]:
        """Get trending topics from Twitter"""
        if not self.twitter_client:
            logger.warning("Twitter client not configured")
            return []
        
        try:
            trends = self.twitter_client.get_place_trends(id=location)
            trending_topics = []
            if trends and len(trends) > 0:
                for idx, trend in enumerate(trends[0]["trends"][:10]):
                    trending_topics.append(TrendingTopic(
                        keyword=trend["name"],
                        trend_score=float(trend.get("tweet_volume", 0) or 0),
                        platform="twitter",
                        source="twitter_api"
                    ))
            return trending_topics
        except Exception as e:
            logger.error(f"Error fetching Twitter trends: {e}")
            return []
    
    async def get_all_trending(self) -> List[TrendingTopic]:
        """Get trending topics from all sources"""
        all_trends = []
        
        # Google Trends
        google_trends = await self.get_google_trends()
        all_trends.extend(google_trends)
        
        # Reddit
        reddit_trends = await self.get_reddit_trending()
        all_trends.extend(reddit_trends)
        
        # Twitter
        twitter_trends = await self.get_twitter_trending()
        all_trends.extend(twitter_trends)
        
        # Sort by trend score
        all_trends.sort(key=lambda x: x.trend_score, reverse=True)
        
        return all_trends


# Global instance
trending_service = TrendingTopicsService()

