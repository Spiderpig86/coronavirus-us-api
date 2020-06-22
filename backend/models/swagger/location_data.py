"""County Model

Model that represents statistics for a given county inside COUNTY_INFO.csv
"""
from typing import Dict, List, Optional

from pydantic import BaseModel

from backend.models.classes.source import Source
from backend.models.swagger.coordinates import Coordinates


class LocationProperties(BaseModel):
    uid: str
    iso2: str
    iso3: str
    code3: str
    fips: str
    county: str
    state: str
    country: str
    coordinates: Coordinates
    combined_key: str
    population: int
