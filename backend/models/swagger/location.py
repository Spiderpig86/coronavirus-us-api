"""Location Model

Generic model to represent a location and the statistics that each location should contain.
"""

from typing import Dict, List, Optional

from pydantic import BaseModel

from backend.models.swagger.history import Timelines
from backend.models.swagger.location_data import LocationProperties
from backend.models.swagger.statistics import Statistics


class Location(BaseModel):
    id: str  # UUID
    country: str
    state: Optional[str]
    county: Optional[str]
    fips: Optional[str]
    uid: Optional[str]
    iso2: Optional[str]
    iso3: Optional[str]
    admin2: Optional[str]
    code3: Optional[str]
    latitude: Optional[str]
    longitude: Optional[str]
    timelines: Optional[Timelines]
    last_updated: str
    latest: Statistics
    properties: Optional[LocationProperties]
