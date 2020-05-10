"""Router

Router for base API endpoints.
"""
from fastapi import APIRouter

from backend.api.routes.counties import all as counties_all
from backend.api.routes.counties import latest as counties_latest
from backend.api.routes.data import sources
from backend.api.routes.health import heartbeat
from backend.api.routes.states import all as states_all
from backend.api.routes.states import latest as states_latest

from backend.core.config.constants import (  # isort:skip
    API_TAG_COUNTIES,
    API_TAG_DATA,
    API_TAG_HEALTH,
    API_TAG_STATES,
)


class Router:
    def __init__(self):
        self.api_router = APIRouter()

        ##########
        # HEALTH #
        ##########
        self.api_router.include_router(
            heartbeat.router, tags=[API_TAG_HEALTH], prefix="/health"
        )

        ############
        # COUNTIES #
        ############
        self.api_router.include_router(
            counties_all.router, tags=[API_TAG_COUNTIES], prefix="/counties"
        )
        self.api_router.include_router(
            counties_latest.router, tags=[API_TAG_COUNTIES], prefix="/counties"
        )

        ##########
        # STATES #
        ##########
        self.api_router.include_router(
            states_all.router, tags=[API_TAG_STATES], prefix="/states"
        )
        self.api_router.include_router(
            states_latest.router, tags=[API_TAG_STATES], prefix="/states"
        )

        ########
        # DATA #
        ########
        self.api_router.include_router(
            sources.router, tags=[API_TAG_DATA], prefix="/data"
        )
