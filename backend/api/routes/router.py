"""Router

Router for base API endpoints.
"""
from fastapi import APIRouter

from backend.api.routes.data import all, latest, sources
from backend.api.routes.health import heartbeat
from backend.core.config.constants import API_TAG_DATA, API_TAG_HEALTH


class Router:
    def __init__(self):
        self.api_router = APIRouter()
        self.api_router.include_router(
            heartbeat.router, tags=[API_TAG_HEALTH], prefix="/health"
        )
        self.api_router.include_router(all.router, tags=[API_TAG_DATA], prefix="/data")
        self.api_router.include_router(
            latest.router, tags=[API_TAG_DATA], prefix="/data"
        )
        self.api_router.include_router(
            sources.router, tags=[API_TAG_DATA], prefix="/data"
        )
