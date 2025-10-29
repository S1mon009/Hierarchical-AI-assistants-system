from fastapi import FastAPI
from src.routes.auth.register import router as register_router

app = FastAPI(title="Hierarchical AI assistants system")
app.include_router(register_router, prefix="/auth", tags=["auth"])
