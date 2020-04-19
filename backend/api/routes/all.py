"""All Endpoint

Endpoint for fetching all information given a source.
"""
from fastapi import APIRouter, HTTPException, Request

from backend.models.endpoints.all import AllResult

######################
# ROUTER DECLARATION #
######################
router = APIRouter()

##########
# ROUTES #
##########
@router.get(
    "/all", response_model=AllResult, name="All", response_model_exclude_unset=True
)
async def get_all(
    request: Request,
    source: str = "nyt",  # TODO: Change to enum
    fips_code: str = None,
    county: str = None,
    state: str = None,
    history: bool = False,
) -> AllResult:

    params_dict = dict(request.query_params)

    params_dict.pop("source", None)
    params_dict.pop("history", None)

    # Fetch data
    data_source_service = await request.state.data_source
    locations = await data_source_service.get_data()
