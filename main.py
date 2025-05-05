"""
Main entry point for the Retail Intelligence Engine API.
"""
import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.serving.inference import router

# Create FastAPI app instance
app = FastAPI(
    title="Retail Intelligence Engine API",
    description="API for retail data analysis and insights",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include the router
app.include_router(router)

def main():
    """
    Main function to run the FastAPI application.
    """
    uvicorn.run(
        "main:app",  # Use the app instance from this module
        host="0.0.0.0",  # Allow external connections
        port=8000,
        reload=True  # Enable auto-reload during development
    )

if __name__ == "__main__":
    main()
