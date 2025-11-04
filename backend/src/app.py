"""Main FastAPI application entry point.

This module initializes the FastAPI application instance and registers
the authentication routes used for user registration and related actions.
It serves as the central setup point for the backend application.
"""
from fastapi import FastAPI
from src.routes.auth.register import router as register_router

app = FastAPI(title="Hierarchical AI assistants system")
app.include_router(register_router, prefix="/auth", tags=["auth"])
