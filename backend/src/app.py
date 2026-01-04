"""Main FastAPI application entry point.

This module initializes the FastAPI application instance and registers
the authentication routes used for user registration and related actions.
It serves as the central setup point for the backend application.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.modules.auth.auth_module import auth_module
from src.modules.users.users_module import users_module
from src.modules.chat.chat_module import chat_module

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
]

app = FastAPI(title="Hierarchical AI assistants system")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_module.router)
app.include_router(users_module.router)
app.include_router(chat_module.router)
