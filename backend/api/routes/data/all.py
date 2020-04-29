"""All Endpoint

Endpoint for fetching all information given a source.
"""
from fastapi import APIRouter, HTTPException, Request

from backend.models.classes.statistics import Statistics
from backend.models.endpoints.all import AllResult
from backend.models.source import Source
from backend.utils.state_abbr import STATE_ABBR__STATE_NAME, get_state_name

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
    source: Source = "nyt",
    fips: str = None,
    county: str = None,
    state: str = None,
    timelines: bool = False,
):

    params_dict = dict(request.query_params)

    # Remove unfiltered parameters
    params_dict.pop("source", None)
    params_dict.pop("timelines", None)

    # Fetch data
    data_source_service = request.state.data_source
    location_data, _ = await data_source_service.get_data()

    # TODO: Refactor filtering
    for key, value in params_dict.items():
        key = key.lower()
        value = value.lower().strip("__")  # Remove access to private/internal fields

        if not value:
            continue

        if key == "state" and value.upper() in STATE_ABBR__STATE_NAME:
            value = get_state_name(value)

        location_data = list(
            filter(
                lambda location: str(getattr(location, key)).lower() == value,
                location_data,
            )
        )

    latest = Statistics(
        confirmed=sum(
            map(lambda location: location.timelines["confirmed"].latest, location_data)
        ),
        deaths=sum(
            map(lambda location: location.timelines["deaths"].latest, location_data)
        ),
    )

    return {
        "latest": latest.to_dict(),
        "locations": [
            location.to_dict(timelines) for location in location_data
        ],  # TODO: Do not hardcode boolean
    }
