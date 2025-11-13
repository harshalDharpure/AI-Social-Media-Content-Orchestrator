"""
Service for social media integrations (Twitter, Instagram, LinkedIn)
"""
import tweepy
import requests
# LinkedIn integration requires OAuth flow
# from linkedin import linkedin
from app.core.config import settings
from app.models.schemas import Platform, PostRequest, PostResponse, ContentStatus
from typing import Optional
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


class SocialMediaService:
    """Service for social media integrations"""
    
    def __init__(self):
        # Initialize Twitter client
        if all([settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET,
                settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET]):
            self.twitter_auth = tweepy.OAuthHandler(
                settings.TWITTER_API_KEY,
                settings.TWITTER_API_SECRET
            )
            self.twitter_auth.set_access_token(
                settings.TWITTER_ACCESS_TOKEN,
                settings.TWITTER_ACCESS_TOKEN_SECRET
            )
            self.twitter_api = tweepy.API(self.twitter_auth)
        else:
            self.twitter_api = None
        
        # Initialize LinkedIn client (requires OAuth flow - simplified for now)
        self.linkedin_enabled = bool(settings.LINKEDIN_ACCESS_TOKEN)
    
    async def post_to_twitter(self, content: str, image_url: Optional[str] = None) -> PostResponse:
        """Post to Twitter"""
        if not self.twitter_api:
            raise Exception("Twitter API not configured")
        
        try:
            # Upload image if provided
            media_ids = None
            if image_url:
                media = self.twitter_api.media_upload(image_url)
                media_ids = [media.media_id]
            
            # Post tweet
            tweet = self.twitter_api.update_status(
                status=content,
                media_ids=media_ids
            )
            
            return PostResponse(
                id=str(uuid.uuid4()),
                content_id="",
                platform=Platform.TWITTER,
                status=ContentStatus.PUBLISHED,
                post_url=f"https://twitter.com/i/web/status/{tweet.id}",
                published_at=datetime.utcnow()
            )
        except Exception as e:
            logger.error(f"Error posting to Twitter: {e}")
            return PostResponse(
                id=str(uuid.uuid4()),
                content_id="",
                platform=Platform.TWITTER,
                status=ContentStatus.FAILED,
                error=str(e)
            )
    
    async def post_to_instagram(self, caption: str, image_url: str) -> PostResponse:
        """Post to Instagram"""
        if not settings.INSTAGRAM_ACCESS_TOKEN or not settings.INSTAGRAM_APP_ID:
            raise Exception("Instagram API not configured")
        
        try:
            # Instagram requires Graph API
            # Step 1: Create media container
            url = f"https://graph.instagram.com/v18.0/{settings.INSTAGRAM_APP_ID}/media"
            
            payload = {
                "caption": caption,
                "image_url": image_url,
                "access_token": settings.INSTAGRAM_ACCESS_TOKEN
            }
            
            response = requests.post(url, json=payload)
            response.raise_for_status()
            
            creation_id = response.json().get("id")
            
            # Step 2: Publish the media
            publish_url = f"https://graph.instagram.com/v18.0/{settings.INSTAGRAM_APP_ID}/media_publish"
            publish_payload = {
                "creation_id": creation_id,
                "access_token": settings.INSTAGRAM_ACCESS_TOKEN
            }
            
            publish_response = requests.post(publish_url, json=publish_payload)
            publish_response.raise_for_status()
            
            post_id = publish_response.json().get("id")
            
            return PostResponse(
                id=str(uuid.uuid4()),
                content_id="",
                platform=Platform.INSTAGRAM,
                status=ContentStatus.PUBLISHED,
                post_url=f"https://www.instagram.com/p/{post_id}/",
                published_at=datetime.utcnow()
            )
        except Exception as e:
            logger.error(f"Error posting to Instagram: {e}")
            return PostResponse(
                id=str(uuid.uuid4()),
                content_id="",
                platform=Platform.INSTAGRAM,
                status=ContentStatus.FAILED,
                error=str(e)
            )
    
    async def post_to_linkedin(self, content: str, image_url: Optional[str] = None) -> PostResponse:
        """Post to LinkedIn"""
        if not self.linkedin_enabled:
            raise Exception("LinkedIn API not configured")
        
        try:
            # LinkedIn post using API (requires proper OAuth setup)
            # This is a simplified version - in production, you need OAuth flow
            url = "https://api.linkedin.com/v2/ugcPosts"
            
            headers = {
                "Authorization": f"Bearer {settings.LINKEDIN_ACCESS_TOKEN}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0"
            }
            
            # Get person URN (this would come from OAuth)
            # For now, using a placeholder
            payload = {
                "author": f"urn:li:person:{settings.LINKEDIN_CLIENT_ID}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": content
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            post_id = result.get("id", "").split(":")[-1] if "id" in result else ""
            
            return PostResponse(
                id=str(uuid.uuid4()),
                content_id="",
                platform=Platform.LINKEDIN,
                status=ContentStatus.PUBLISHED,
                post_url=f"https://www.linkedin.com/feed/update/{post_id}/" if post_id else None,
                published_at=datetime.utcnow()
            )
        except Exception as e:
            logger.error(f"Error posting to LinkedIn: {e}")
            return PostResponse(
                id=str(uuid.uuid4()),
                content_id="",
                platform=Platform.LINKEDIN,
                status=ContentStatus.FAILED,
                error=str(e)
            )
    
    async def post(self, request: PostRequest, content: str) -> PostResponse:
        """Post content to specified platform"""
        try:
            if request.platform == Platform.TWITTER:
                return await self.post_to_twitter(content, request.image_url)
            elif request.platform == Platform.INSTAGRAM:
                if not request.image_url:
                    raise Exception("Instagram requires an image")
                return await self.post_to_instagram(content, request.image_url)
            elif request.platform == Platform.LINKEDIN:
                return await self.post_to_linkedin(content, request.image_url)
            else:
                raise Exception(f"Unsupported platform: {request.platform}")
        except Exception as e:
            logger.error(f"Error posting to {request.platform}: {e}")
            raise


# Global instance
social_media_service = SocialMediaService()

