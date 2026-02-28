"""FastAPI Application - Main entry point"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import modes

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

# Include routers
app.include_router(modes.router, prefix="/api", tags=["modes"])

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "Love Debugging Lab v2.0",
        "version": "2.0.0",
        "endpoints": {
            "mode1": "/api/mode1/love-reading",
            "mode2": "/api/mode2/celebrity-match",
            "mode3": "/api/mode3/couple-match"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
