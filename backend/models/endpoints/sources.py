"""Sources Response Model

API Model for Sources endpoint.
"""
from pydantic import BaseModel

from typing import List



class SourceResult(BaseModel):
    sources: List[str]
