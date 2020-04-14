"""Location Model

Generic model to represent a location and the statistics that each location should contain.
"""

from datetime import datetime
from pydantic import BaseModel
from typing import Dict, List

from .history import History
from .statistic import Statistics

class Location(BaseModel):
    id: str # UUID
    country: str
    state: str
    fips: str
    history: History
    last_updated: datetime
    latest: Statistics