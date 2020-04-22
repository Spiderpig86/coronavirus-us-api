"""Statistics

Model representing Coronavirus stats of a location for a specific category at a given time.
"""

from pydantic import BaseModel


class Statistics(BaseModel):
    confirmed: int
    deaths: int
