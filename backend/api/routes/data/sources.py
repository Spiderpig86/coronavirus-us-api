"""Sources Route

Route that returns list of supported sources.
"""
from fastapi import APIRouter, HTTPException, Request

from backend.models.source import Source

######################
# ROUTER DECLARATION #
######################
router = APIRouter()

##########
# ROUTES #
##########
@router.get(
    "/sources",
    response_model=object,
    name="Sources",
    response_model_exclude_unset=True,
)
async def get_sources(
    request: Request, source: Source = "nyt"
):  # TODO: Do not hardcode default
    # TODO: Stubbing

    return None
