"""Events

File containing lifecycle event handlers for the server.
"""
from typing import Callable

from fastapi import FastAPI
from loguru import logger

from backend.core.utils.webclient import setup_webclient, teardown_webclient


def startup_handler(app: FastAPI) -> Callable:
    async def startup() -> None:
        logger.info("Server starting up...")
        # Other callbacks
        await setup_webclient()

    return startup


def shutdown_handler(app: FastAPI) -> Callable:
    async def shutdown() -> None:
        logger.info("Server is shutting down...")
        # Cleanup tasks
        await teardown_webclient()

    return shutdown
