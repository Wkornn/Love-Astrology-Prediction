"""FastAPI Application - Main entry point"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import logging
from .api.routes import modes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Love Debugging Lab v2.0",
    description="Astrological love compatibility analysis API",
    version="2.0.0"
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch all unhandled exceptions and return standardized error (Demo Safety Mode)"""
    logger.error(f"Unhandled exception on {request.url.path}: {str(exc)}", exc_info=True)
    
    # Never crash - always return a response
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "mode": None,
            "error": "System temporarily unavailable",
            "details": "Please try again. If issue persists, contact support.",
            "timestamp": datetime.utcnow().isoformat() + 'Z'
        }
    )

# Include routers
app.include_router(modes.router, prefix="/api", tags=["modes"])

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "Love Debugging Lab v2.0",
        "version": "2.0.0",
        "status": "operational",
        "endpoints": {
            "mode1": "/api/mode1/love-reading",
            "mode2": "/api/mode2/celebrity-match",
            "mode3": "/api/mode3/couple-match"
        },
        "timestamp": datetime.utcnow().isoformat() + 'Z'
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + 'Z'
    }
