"""Main entry point to the API.

Coronavirus-us is an API dedicated to fetching live and historical statistics on infections and deaths on a country, state, and county level.
"""
import os

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from backend.api.routes.router import Router
from backend.core.events import shutdown_handler, startup_handler
from backend.services.data_service import get_data_source

from backend.core.config.constants import (  # isort:skip
    API_PREFIX,
    APP_DEBUG,
    APP_DESCRIPTION,
    APP_NAME,
    APP_VERSION,
)


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

    @fast_api.middleware("http")
    async def inject_data_source(request: Request, next) -> Response:
        """Injects data source service based on given data source parameter.
        
        Arguments:
            request {Request} -- endpoint request object.
            next {function} -- next function in service chain.
        
        Returns:
            Response -- Return updated response with new data service in request state.
        """
        source_param = request.query_params.get("source", default="nyt")
        data_source = get_data_source(source_param)

        # Handle incorrect source
        if not data_source:
            return Response(
                f"The given datasource '{source_param}' is not valid.", status_code=400
            )

        # Inject data source service
        request.state.data_source = data_source

        logger.info(f"Data source service {data_source.__class__.name} injected...")
        response = await next(request)
        return response

    return fast_api


api = get_api()

if __name__ == "__main__":
    uvicorn.run(
        "backend:main:api", host="127.0.0.1", port=int(), log_level="info",
    )
