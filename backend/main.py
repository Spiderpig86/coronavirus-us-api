"""Main entry point to the API.

Coronavirus-us is an API dedicated to fetching live and historical statistics on infections and deaths on a country, state, and county level.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn

from backend.api.routes.router import Router
from backend.core.config.constants import (
    API_PREFIX,
    APP_NAME,
    APP_DESCRIPTION,
    APP_VERSION,
    APP_DEBUG,
)
from backend.core.events import startup_handler, shutdown_handler

def get_api() -> FastAPI:
    fast_api = FastAPI(
        title=APP_NAME,
        description=APP_DESCRIPTION,
        version=APP_VERSION,
        debug=APP_DEBUG,
        docs_url="/",
        redoc_url="/docs",
    )

    router = Router()
    fast_api.include_router(router.api_router, prefix=f"{API_PREFIX}")

    fast_api.add_event_handler("startup", startup_handler(fast_api))
    fast_api.add_event_handler("shutdown", shutdown_handler(fast_api))

    ##############
    # MIDDLEWARE #
    ##############
    fast_api.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return fast_api

api = get_api()

if __name__ == "__main__":
    uvicorn.run(
        "backend:main:api", host="127.0.0.1", port=int(), log_level="info",
    )
