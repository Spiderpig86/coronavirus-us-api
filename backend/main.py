"""Main entry point to the API.

Coronavirus-us is an API dedicated to fetching live and historical statistics on infections and deaths on a country, state, and county level.
"""
import json
import os

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from backend.api.routes.router import Router
from backend.core.events import shutdown_handler, startup_handler
from backend.models.classes.source import Source
from backend.utils.containers import Container, DataSourceContainer

from backend.core.config.constants import (  # isort:skip
    CONFIG_APP_HOST,
    CONFIG_APP_LOG_LEVEL,
    CONFIG_APP_PORT,
    TAGS_METADATA,
)

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
        openapi_tags=TAGS_METADATA,
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
    async def inject_services(request: Request, next) -> Response:
        """Injects data source service based on given data source parameter.
        
        Arguments:
            request {Request} -- endpoint request object.
            next {function} -- next function in service chain.
        
        Returns:
            Response -- Return updated response with new data service in request state.
        """
        source_param = request.query_params.get("source", default=Source.NYT)

        # Handle incorrect source
        if source_param not in Source.list():
            return Response(
                json.dumps(
                    {
                        "error": "Invalid Data Source",
                        "message": f"The given datasource '{source_param}' is not valid.",
                    }
                ),
                media_type="application/json",
                status_code=400,
            )

        # Inject services
        data_source = DataSourceContainer.data_sources().get_data_source(source_param)
        request.state.data_source = data_source
        request.state.location_data_service = (
            DataSourceContainer.location_data_service()
        )

        logger.info(f"Data source service {data_source.__class__.__name__} injected...")
        response = await next(request)
        return response

    return fast_api


api = get_api()

if __name__ == "__main__":
    uvicorn.run(
        "backend:main:api",
        host=CONFIG_APP_HOST,
        port=int(CONFIG_APP_PORT),
        log_level=CONFIG_APP_LOG_LEVEL,
    )
