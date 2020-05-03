"""Sources Response Model

API Model for Sources endpoint.
"""
from typing import List

from pydantic import BaseModel


class SourceResult(BaseModel):
    sources: List[str]
