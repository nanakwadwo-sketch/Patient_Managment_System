from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

# This module contains exception handlers for the FastAPI application.
# It defines custom exception handlers for HTTP exceptions and general exceptions.
def add_exception_handlers(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

    # General exception handler for unhandled exceptions
    # This handler catches all unhandled exceptions and returns a 500 Internal Server Error response.
    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )