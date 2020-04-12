"""Main entry point to the API.

TODO: App description
"""
from fastapi import FastAPI

from backend.api.routes.router import Router
from backend.core.config.constants import (
    API_PREFIX, APP_NAME, APP_VERSION, APP_DEBUG
)
from backend.core.events import (
    startup_handler, shutdown_handler
)

def get_api() -> FastAPI:
    fast_api = FastAPI(
        title=APP_NAME,
        version=APP_VERSION,
        debug=APP_DEBUG
    )

    router = Router()
    fast_api.include_router(router.api_router, prefix=f'{API_PREFIX}')

    fast_api.add_event_handler('startup', startup_handler(fast_api))
    fast_api.add_event_handler('shutdown', shutdown_handler(fast_api))

    return fast_api

api = get_api()