"""Application entry point for running the FastAPI server.

This module starts the FastAPI application using Uvicorn,
loading host and port configuration from the Settings object.
"""

import uvicorn
from src.config.config import settings
from src.app import app

if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)
