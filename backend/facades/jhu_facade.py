"""JHU Facade

Class that interfaces with jhu_service.py to aggregate data.
"""

import asyncio

from backend.core.config.constants import DATA_ENDPOINTS
from backend.facades.facade import DataSourceFacade
from backend.models.classes.category import Category
from backend.models.classes.location import JhuLocation
from backend.models.classes.location_data import LocationProperties
from backend.models.classes.statistics import Statistics
from backend.services.jhu_service import JhuDataService
from backend.services.location_data_service import LocationDataService
from backend.utils.functions import Functions


class JhuFacade(DataSourceFacade):
    def __init__(self):
        self.DATA_SERVICE = JhuDataService()
        self.LOCATION_SERVICE = LocationDataService()
        self.ENDPOINT = DATA_ENDPOINTS.get(self.__class__.__name__)

    async def get_state_data(self):
        promises = await asyncio.gather(
            self.DATA_SERVICE.get_data(self.ENDPOINT),
            self.LOCATION_SERVICE.get_state_data(),
        )

        results_by_county, last_updated = promises[0]
        state_data = promises[1]

        # Aggregate results on a per state basis
        state_results = {}
        for result in results_by_county:
            id = result.id.split("@")[:2]
            key = (id[1], id[0])

            if key not in state_results:
                properties_for_state = (
                    state_data[key] if key in state_data else LocationProperties()
                )
                state_results[key] = JhuLocation(
                    id=Functions.to_location_id(key),
                    uid=properties_for_state.UID,
                    iso2=properties_for_state.iso2,
                    iso3=properties_for_state.iso3,
                    code3=properties_for_state.code3,
                    fips=properties_for_state.fips,
                    admin2=properties_for_state.admin2,
                    state=result.state,
                    country=result.country,
                    latitude=properties_for_state.coordinates.latitude,
                    longitude=properties_for_state.coordinates.longitude,
                    last_updated=last_updated,
                    timelines={"confirmed": {}, "deaths": {}},
                    latest=None,
                )

            jhu_location = state_results[key]
            for confirmed_date, count in result.timelines["confirmed"].category.items():
                value = jhu_location.timelines["confirmed"].get(confirmed_date, 0)
                jhu_location.timelines["confirmed"][confirmed_date] = value + count

            for deaths_date, count in result.timelines["deaths"].category.items():
                value = jhu_location.timelines["deaths"].get(deaths_date, 0)
                jhu_location.timelines["deaths"][deaths_date] = value + count

        # Remap dicts to Category
        for _, state in state_results.items():
            state.timelines["confirmed"] = Category(state.timelines["confirmed"])
            state.timelines["deaths"] = Category(state.timelines["deaths"])
            state.latest = Statistics(
                state.timelines["confirmed"].latest, state.timelines["deaths"].latest
            ).to_dict()

        return state_results.values(), last_updated

    async def get_county_data(self):
        return await self.DATA_SERVICE.get_data(self.ENDPOINT)
