"""JHU Facade

Class that interfaces with jhu_service.py to aggregate data.
"""

import asyncio
from typing import List

from backend.core.config.constants import DATA_ENDPOINTS
from backend.facades.facade import DataSourceFacade
from backend.models.classes.category import Category
from backend.models.classes.location import JhuLocation
from backend.models.classes.location_properties import LocationProperties
from backend.models.classes.statistics import Statistics
from backend.services.jhu_service import JhuDataService
from backend.services.location_data_service import LocationDataService
from backend.utils.functions import Functions


class JhuFacade(DataSourceFacade):
    def __init__(self):
        from backend.utils.containers import DataSourceContainer
        self.DATA_SERVICE = JhuDataService()
        self.LOCATION_SERVICE = DataSourceContainer.location_data_service()
        self.ENDPOINT = DATA_ENDPOINTS.get(self.__class__.__name__)

    async def get_country_data(self) -> (List[JhuLocation], str):
        """Notes: Function currently designed only for US data
        """
        promises = await asyncio.gather(self.DATA_SERVICE.get_data(self.ENDPOINT),)

        results_by_county, last_updated = promises[0]

        location_properties = JhuLocation(
            id=Functions.to_location_id(("US",)),
            uid="840",
            iso2="US",
            iso3="USA",
            code3="USA",
            fips="",
            county="",
            state="",
            country="US",
            latitude="37.0902",  # TODO: Do not hardcode
            longitude="-95.7129",
            last_updated=last_updated,
            timelines={"confirmed": {}, "deaths": {}},
            latest=None,
        )

        for result in results_by_county:
            for confirmed_date, count in result.timelines["confirmed"].category.items():
                value = location_properties.timelines["confirmed"].get(
                    confirmed_date, 0
                )
                location_properties.timelines["confirmed"][confirmed_date] = (
                    value + count
                )

            for deaths_date, count in result.timelines["deaths"].category.items():
                value = location_properties.timelines["deaths"].get(deaths_date, 0)
                location_properties.timelines["deaths"][deaths_date] = value + count

        location_properties.timelines["confirmed"] = Category(
            location_properties.timelines["confirmed"]
        )
        location_properties.timelines["deaths"] = Category(
            location_properties.timelines["deaths"]
        )
        location_properties.latest = Statistics(
            location_properties.timelines["confirmed"].latest,
            location_properties.timelines["deaths"].latest,
        ).to_dict()

        return [location_properties], last_updated

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
            key = tuple(result.id.split("@")[:2])

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
                    county=properties_for_state.admin2,
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
