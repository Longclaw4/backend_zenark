"""
Simple Request Queue to Handle OpenAI Rate Limits
Queues requests and processes them at 3 RPM (free tier limit)
"""

import asyncio
from collections import deque
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class RequestQueue:
    def __init__(self, max_requests_per_minute=3):
        self.queue = deque()
        self.max_rpm = max_requests_per_minute
        self.request_times = deque()
        self.processing = False
    
    async def add_request(self, request_func, *args, **kwargs):
        """Add a request to the queue and wait for it to be processed"""
        future = asyncio.Future()
        self.queue.append((request_func, args, kwargs, future))
        
        # Start processing if not already running
        if not self.processing:
            asyncio.create_task(self._process_queue())
        
        # Wait for this request to be processed
        return await future
    
    async def _process_queue(self):
        """Process queued requests at max_rpm rate"""
        self.processing = True
        
        while self.queue:
            # Clean up old request times (older than 1 minute)
            now = datetime.now()
            while self.request_times and self.request_times[0] < now - timedelta(minutes=1):
                self.request_times.popleft()
            
            # Check if we can make a request
            if len(self.request_times) < self.max_rpm:
                # Process next request
                request_func, args, kwargs, future = self.queue.popleft()
                
                try:
                    # Execute the request
                    result = await request_func(*args, **kwargs)
                    future.set_result(result)
                    
                    # Record request time
                    self.request_times.append(datetime.now())
                    
                    logger.info(f"✅ Processed request. Queue size: {len(self.queue)}")
                    
                except Exception as e:
                    future.set_exception(e)
                    logger.error(f"❌ Request failed: {e}")
            
            else:
                # Wait before checking again
                wait_time = 60 / self.max_rpm  # seconds between requests
                logger.info(f"⏳ Rate limit reached. Waiting {wait_time}s. Queue: {len(self.queue)}")
                await asyncio.sleep(wait_time)
        
        self.processing = False

# Global queue instance
openai_queue = RequestQueue(max_requests_per_minute=3)
