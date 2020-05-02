"""County Model

Model that represents statistics for a given county inside COUNTY_INFO.csv
"""
from typing import Dict, List, Optional

from pydantic import BaseModel

from backend.models.classes.coordinates import Coordinates
from backend.models.source import Source


class County(BaseModel):
    UID: int
    iso2: str
    iso3: str
    code3: int
    fips: str
    admin2: str
    state: str
    country: str
    coordinates: Coordinates
    combined_key: str
    population: int
