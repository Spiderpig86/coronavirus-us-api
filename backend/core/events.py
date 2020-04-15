"""Events

File containing lifecycle event handlers for the server.
"""
from typing import Callable

from fastapi import FastAPI
from loguru import logger


def startup_handler(app: FastAPI) -> Callable:
    def startup() -> None:
        logger.info("Server starting up...")
        # Other callbacks

    return startup


def shutdown_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        logger.info("Server is shutting down...")
        # Cleanup tasks

    return shutdown
