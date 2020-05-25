"""State Service

Service used for returning state information.
"""
import csv

from asyncache import cached
from cachetools import TTLCache
from loguru import logger

from backend.core.config.constants import DATA_ENDPOINTS
from backend.core.utils import webclient
from backend.models.classes.coordinates import Coordinates
from backend.models.classes.location_properties import LocationProperties


class LocationDataService(object):
    def __init__(self):
        self.ENDPOINT = DATA_ENDPOINTS.get(self.__class__.__name__)

    @cached(cache=TTLCache(maxsize=1024, ttl=36000))
    async def get_state_data(self):
        csv_data = ""

        logger.info("Fetching CSV data for states...")

        async with webclient.WEBCLIENT.get(
            f"{self.ENDPOINT}/STATE_INFO.csv"
        ) as response:
            csv_data = await response.text()

        parsed_data = list(csv.DictReader(csv_data.splitlines()))

        state_map = {}

        for state_data in parsed_data:
            state_map[self._state_data_id(state_data)] = LocationProperties(
                state_data["UID"],
                state_data["iso2"],
                state_data["iso3"],
                state_data["code3"],
                state_data["FIPS"],
                state_data["Admin2"],
                state_data["State"],
                state_data["Country"],
                Coordinates(state_data["Latitude"], state_data["Longitude"]),
                state_data["Formal_Name"],
                state_data["Population"],
            )

        return state_map

    @cached(cache=TTLCache(maxsize=1024, ttl=36000))
    async def get_county_data(self):
        csv_data = ""

        logger.info("Fetching CSV data for counties...")

        async with webclient.WEBCLIENT.get(
            f"{self.ENDPOINT}/COUNTY_INFO.csv"
        ) as response:
            csv_data = await response.text()

        parsed_data = list(csv.DictReader(csv_data.splitlines()))

        county_map = {}

        for county_data in parsed_data:
            county_map[self._county_data_id(county_data)] = LocationProperties(
                county_data["UID"],
                county_data["iso2"],
                county_data["iso3"],
                county_data["code3"],
                county_data["FIPS"],
                county_data["Admin2"],
                county_data["State"],
                county_data["Country"],
                Coordinates(county_data["Latitude"], county_data["Longitude"]),
                county_data["Formal_Name"],
                int(county_data["Population"] or 0),
            )

        return county_map

    def _state_data_id(self, state_data):

        return (state_data["State"], state_data["Country"])

    def _county_data_id(self, county_data):

        return (
            county_data["Admin2"].lower(),
            county_data["State"],
            county_data["Country"],
        )
