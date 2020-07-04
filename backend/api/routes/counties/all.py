"""All Endpoint

Endpoint for fetching all information given a source.
"""
import time

from fastapi import APIRouter, HTTPException, Request
from loguru import logger

from backend.models.classes.source import Source
from backend.models.classes.statistics import Statistics
from backend.models.swagger.endpoints.all import AllResult
from backend.utils.functions import Functions
from backend.utils.state_abbr import STATE_ABBR__STATE_NAME, get_state_name

######################
# ROUTER DECLARATION #
######################
router = APIRouter()

##########
# ROUTES #
##########
@router.get("/all", name="All", response_model_exclude_unset=True)
async def get_all(
    request: Request,
    source: Source = "nyt",
    fips: str = None,
    county: str = None,
    state: str = None,
    timelines: bool = False,
    properties: bool = False,
):

    params_dict = dict(request.query_params)

    # Remove unfiltered parameters
    params_dict.pop("source", None)
    params_dict.pop("timelines", None)
    params_dict.pop("properties", None)

    # Fetch data
    data_source_service = request.state.data_source
    location_data, _ = await data_source_service.get_county_data()

    # TODO: Refactor filtering
    for key, value in params_dict.items():
        key = key.lower()
        value = value.lower().strip(
            "__"
        )  # Remove access to private/internal fields, even if key uses underscores

        if key == "state" and value.upper() in STATE_ABBR__STATE_NAME:
            value = get_state_name(value)

        location_data = list(
            filter(
                lambda location: str(Functions.try_getattr(location, key))
                == "__IGNORE__"
                or str(Functions.try_getattr(location, key)).lower() == str(value),
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

    county_data_map = None
    if properties:
        location_data_service = request.state.location_data_service
        _start = time.time() * 1000.0
        county_data_map = await location_data_service.get_county_data()
        _end = time.time() * 1000.0
        logger.info(f"Elapsed for all endpoint {str(_end-_start)}ms")

    locations_response = []
    for location in location_data:
        if properties and location.county != "Unknown":
            location.set_properties(
                county_data_map[
                    (location.country, location.state, location.county.lower(),)
                ].to_dict()
            )
        result = location.to_dict(timelines, properties)

        locations_response.append(result)

    return {
        "latest": latest.to_dict(),
        "locations": locations_response,
    }
