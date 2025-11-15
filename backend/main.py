"""Application entry point for running the FastAPI server.

This module serves as the main execution script for starting the FastAPI
application using Uvicorn. It loads configuration values such as host and port
from the Settings object defined in `src.config.config` and runs the server.

When executed directly, this module launches the backend service that provides
the REST API for the Hierarchical AI Assistants System.
"""
import uvicorn
from src.config import settings
from src.app import app

if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port)
