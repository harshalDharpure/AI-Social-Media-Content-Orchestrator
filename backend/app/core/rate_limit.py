"""
Rate limiting middleware
"""
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, Tuple
import time

# In-memory rate limit storage (use Redis in production)
rate_limit_store: Dict[str, Tuple[int, datetime]] = defaultdict(lambda: (0, datetime.utcnow()))


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware"""
    
    def __init__(self, app, calls: int = 100, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period
    
    async def dispatch(self, request: Request, call_next):
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"
        
        # Check rate limit
        if not self._check_rate_limit(client_ip):
            return Response(
                content="Rate limit exceeded",
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                headers={"Retry-After": str(self.period)}
            )
        
        # Process request
        response = await call_next(request)
        return response
    
    def _check_rate_limit(self, client_ip: str) -> bool:
        """Check if client has exceeded rate limit"""
        now = datetime.utcnow()
        count, reset_time = rate_limit_store[client_ip]
        
        # Reset if period has passed
        if now > reset_time:
            rate_limit_store[client_ip] = (1, now + timedelta(seconds=self.period))
            return True
        
        # Check if limit exceeded
        if count >= self.calls:
            return False
        
        # Increment count
        rate_limit_store[client_ip] = (count + 1, reset_time)
        return True


def get_rate_limit_middleware(calls: int = 100, period: int = 60):
    """Get rate limit middleware"""
    return lambda app: RateLimitMiddleware(app, calls=calls, period=period)

