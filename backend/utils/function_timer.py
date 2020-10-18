import functools
import time

from loguru import logger


def timed(description: str):  # Allows for passing in args to our decorator
    """Function decorator to time function execution.

    Arguments:
        description {str} -- message to log to console.
    """

    def decorator(function):
        @functools.wraps(function)  # Preserve function identity
        def inner(*args, **kwargs):
            _start = time.time() * 1000.0
            result = function(*args, **kwargs)
            _end = time.time() * 1000.0
            logger.info(f"{description} {str(_end-_start)}ms")
            return result

        return inner

    return decorator


def async_timed(description: str):  # Allows for passing in args to our decorator
    """Function decorator to time async function execution.

    Arguments:
        description {str} -- message to log to console.
    """

    def decorator(function):
        @functools.wraps(function)  # Preserve function identity
        async def inner(*args, **kwargs):
            _start = time.time() * 1000.0
            result = await function(*args, **kwargs)
            _end = time.time() * 1000.0
            logger.info(f"{description} {str(_end-_start)}ms")
            return result

        return inner

    return decorator
