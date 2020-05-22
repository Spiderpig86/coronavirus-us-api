"""Deaths Route

Route that returns time series for deaths.
"""
from fastapi import APIRouter, HTTPException, Request

from backend.models.swagger.source import Source

######################
# ROUTER DECLARATION #
######################
router = APIRouter()

##########
# ROUTES #
##########
@router.get(
    "/deaths", response_model=object, name="Deaths", response_model_exclude_unset=True,
)
async def get_deaths(
    request: Request, source: Source = "nyt"
):  # TODO: Do not hardcode default
    # TODO: Stubbing

    return None
