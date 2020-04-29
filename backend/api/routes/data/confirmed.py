"""Confirmed Route

Route that returns time series for confirmed cases.
"""
from fastapi import APIRouter, HTTPException, Request

######################
# ROUTER DECLARATION #
######################
router = APIRouter()

##########
# ROUTES #
##########
@router.get(
    "/confirmed",
    response_model=object,
    name="Confirmed",
    response_model_exclude_unset=True,
)
async def get_confirmed(request: Request, source: Source = "nyt"): # TODO: Do not hardcode default
    # TODO: Stubbing

    return None
