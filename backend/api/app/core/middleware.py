from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings


def add_cors_middleware(app: FastAPI):
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.BACKEND_CORS_ORIGINS,
            allow_methods=["*"],
            allow_credentials=True,
            allow_headers=["*"],
        )
