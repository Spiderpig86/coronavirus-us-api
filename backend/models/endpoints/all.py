"""All Response Model

API model for All endpoint.
"""
from typing import List

from pydantic import BaseModel

from backend.models.location import Location
from backend.models.statistic import Statistics


class AllResult(BaseModel):
    latest: Statistics
    locations: List[Location] = []
