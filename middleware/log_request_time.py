from fastapi import Request
import time
import logging

# This middleware logs the time taken to process each request.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Middleware to log request time
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Request: {request.method} {request.url.path} completed in {duration:.2f} seconds")
    return response