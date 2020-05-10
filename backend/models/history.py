"""History

Model representing historical data for a category at a location and a group of HistoricalCategories
"""
from typing import Dict, Optional

from pydantic import BaseModel


class Category(BaseModel):
    history: Dict[str, int] = {}  # https://docs.python.org/3/library/typing.html
    latest: int


class Timelines(BaseModel):
    confirmed: Category
    deaths: Category
    recovered: Optional[Category]
    active: Optional[Category]
    incident_rate: Optional[Category]
    tested: Optional[Category]
    hospitalized: Optional[Category]
    mortality_rate: Optional[Category]
    testing_rate: Optional[Category]
    hospitalization_rate: Optional[Category]
