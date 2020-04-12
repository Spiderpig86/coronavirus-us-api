"""Heartbeat Model

API Models for Heartbeat endpoint.
"""
from pydantic import BaseModel


class HeartbeatResult(BaseModel):
    is_alive: bool
