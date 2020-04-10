"""Main entry point to the API.

TODO: App description
"""
from fastapi import FastAPI

app = FastAPI()

# TODO: Remove after testing
@app.get('/ping/')
async def ping():
    """Ping call for tesing.
    """
    return {
        'status': 'OK'
    }