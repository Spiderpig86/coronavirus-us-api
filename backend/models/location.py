"""Location Model

Generic model to represent a location and the statistics that each location should contain.
"""

from datetime import datetime
from typing import Dict, List

from pydantic import BaseModel

from .history import History
from .statistics import Statistics


class Location(BaseModel):
    id: str  # UUID
    country: str
    state: str
    county: str
    fips: str
    history: History
    last_updated: datetime
    latest: Statistics
