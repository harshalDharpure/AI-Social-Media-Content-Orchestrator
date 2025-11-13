"""
Task scheduler for content publishing
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
import logging

logger = logging.getLogger(__name__)

# Global scheduler
scheduler = None


def init_scheduler():
    """Initialize task scheduler"""
    global scheduler
    
    jobstores = {
        'default': MemoryJobStore()
    }
    
    executors = {
        'default': ThreadPoolExecutor(20)
    }
    
    job_defaults = {
        'coalesce': False,
        'max_instances': 3
    }
    
    scheduler = AsyncIOScheduler(
        jobstores=jobstores,
        executors=executors,
        job_defaults=job_defaults,
        timezone='UTC'
    )
    
    scheduler.start()
    logger.info("Scheduler initialized and started")


def get_scheduler():
    """Get scheduler instance"""
    return scheduler

