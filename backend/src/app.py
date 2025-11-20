"""Main FastAPI application entry point.

This module initializes the FastAPI application instance and registers
the authentication routes used for user registration and related actions.
It serves as the central setup point for the backend application.
"""
from fastapi import FastAPI
from src.modules.auth.auth_module import auth_module


print(auth_module)

app = FastAPI(title="Hierarchical AI assistants system")
app.include_router(auth_module.router)
