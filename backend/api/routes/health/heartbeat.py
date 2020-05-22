"""Heatbeat Endpoint

Endpoint that will be used to monitor uptime and latency of service.
"""
from fastapi import APIRouter

from backend.models.swagger.endpoints.heartbeat import HeartbeatResult

######################
# ROUTER DECLARATION #
######################
router = APIRouter()

##########
# ROUTES #
##########
@router.get("/heartbeat", response_model=HeartbeatResult, name="heartbeat")
def get_heartbeat() -> HeartbeatResult:
    heartbeat = HeartbeatResult(is_alive=True)
    return heartbeat
