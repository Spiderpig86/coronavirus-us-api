"""Sources Route

Route that returns list of supported sources.
"""
from fastapi import APIRouter, HTTPException, Request

from backend.models.swagger.endpoints.sources import SourceResult
from backend.models.swagger.source import Source

######################
# ROUTER DECLARATION #
######################
router = APIRouter()

##########
# ROUTES #
##########
@router.get(
    "/sources",
    response_model=SourceResult,
    name="Sources",
    response_model_exclude_unset=True,
)
async def get_sources(request: Request):
    return {"sources": Source.list()}
