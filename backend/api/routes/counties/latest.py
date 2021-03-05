"""Latest Route

Route that returns the latest statistics for a given data source.
"""
from fastapi import APIRouter, HTTPException, Request

from backend.models.classes.source import Source
from backend.models.classes.statistics import Statistics
from backend.models.swagger.endpoints.latest import LatestResult

######################
# ROUTER DECLARATION #
######################
router = APIRouter()

##########
# ROUTES #
##########
@router.get(
    "/latest",
    response_model=LatestResult,
    name="Latest",
    response_model_exclude_unset=True,
)
async def get_latest(
    request: Request, source: Source = Source.NYT
):  # TODO: Do not hardcode default
    data_source_service = request.state.data_source
    location_data, last_updated = await data_source_service.get_country_data()

    latest_dict = Statistics(
        confirmed=sum(
            map(lambda location: location.timelines["confirmed"].latest, location_data)
        ),
        deaths=sum(
            map(lambda location: location.timelines["deaths"].latest, location_data)
        ),
    ).to_dict()

    return {"latest": latest_dict, "last_updated": last_updated}
