"""Latest Response Model

API Model for Latest endpoint.
"""
from pydantic import BaseModel

from backend.models.statistics import Statistics

class LatestResult(BaseModel):
    latest: Statistics
    last_updated: str