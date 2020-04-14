"""History

Model representing historical data for a category at a location and a group of HistoricalCategories
"""
from pydantic import BaseModel
from typing import Dict

class Category(BaseModel):
    history: Dict[str, int] = {} # https://docs.python.org/3/library/typing.html
    latest: int

class History(BaseModel):
    confirmed: Category
    deaths: Category