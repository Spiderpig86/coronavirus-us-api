"""Jhu Information Retriever

Fetches Coronavirus statistics updated by JHU CSSEGSI.
Data source can be found here: https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data
"""
import csv
import time
from datetime import datetime
from typing import List

from asyncache import cached
from cachetools import TTLCache
from loguru import logger

from dateutil.parser import parse

from backend.core.config.constants import DATA_ENDPOINTS
from backend.core.utils import webclient
from backend.models.classes.category import Category
from backend.models.classes.statistics import Statistics
from backend.models.history import Timelines
from backend.models.classes.location import JhuLocation

class JhuDataService(object):
    def __init__(self):
        self.ENDPOINT = DATA_ENDPOINTS.get(self.__class__.__name__)

    # TODO: Get states
    async def get_state_data(self):
        return None

    # TODO: Get counties
    async def get_county_data(self):
        return self._get_data(self.ENDPOINT)

    @cached(cache=TTLCache(maxsize=1024, ttl=3600))
    async def _get_data(self, endpoint: str):
        """Method that retrieves data from JHU CSSEGSI.
        
        Arguments:
            endpoint {str} -- string that represents endpoint to get data from.

        Returns:
            Location[], str -- returns list of location stats and the last updated date.
        """
        location_result = {} # Store the final map of datapoints
        location_result = self._get_by_stat("confirmed", location_result)
        location_result = self._get_by_stat("deaths", location_result)

        locations = []
        last_updated = datetime.utcnow().isoformat() + "Z"  # TODO: Util function

        for location_tuple, events, in location_result.items():
            confirmed_map = events["confirmed"]
            deaths_map = events["deaths"]

            confirmed = Category(
                {
                    datetime.strptime(date, "%Y-%m-%d").isoformat() + "Z": amount
                    for date, amount in confirmed_map.items()
                }
            )

            deaths = Category(
                {
                    datetime.strptime(date, "%Y-%m-%d").isoformat() + "Z": amount
                    for date, amount in deaths_map.items()
                }
            )

            locations.append(
                JhuLocation(
                    id=self._location_id(location_tuple),
                    uid=location_result["UID"],
                    iso2=location_result["iso2"],
                    iso3=location_result["iso3"],
                    code3=location_result["code3"],
                    fips=location_result["FIPS"],
                    county=location_result["Admin2"],
                    state=location_result["Province_State"],
                    country=location_result["Country_Region"],
                    latitude=location_result["Lat"],
                    longitude=location_result["Long_"],
                    last_updated=last_updated,
                    timelines={"confirmed": confirmed, "deaths": deaths},
                    latest=Statistics(
                        confirmed=confirmed.latest,
                        deaths=deaths.latest
                    )
                )
            )

        logger.info("Finished transforming JHU results.")
        return locations, last_updated

    async def _get_by_stat(self, stat: str, location_result: dict): # TODO: Change stat to enum

        # TODO: Log
        endpoint = f"{self.ENDPOINT}time_series_covid19_{stat}_us.csv"

        csv_data = ""
        logger.info("Fetching JHU data...")

        # https://docs.aiohttp.org/en/stable/client_quickstart.html#make-a-request
        async with webclient.WEBCLIENT.get(endpoint) as response:
            csv_data = await response.text()

        for timestamp in csv_data:
            location_id = location_id = (
                self._get_field_from_map(timestamp, "Admin2"),
                self._get_field_from_map(timestamp, "Province_State"),
                self._get_field_from_map(timestamp, "FIPS"),
            )

            print(timestamp.items())
            dates = self._filter_date_columns(timestamp.items())

            if location_id not in location_result:
                location_result[location_id] = {
                    "UID": location_result["UID"],
                    "iso2": location_result["iso2"],
                    "iso3": location_result["iso3"],
                    "code3": location_result["code3"],
                    "FIPS": location_result["FIPS"],
                    "Admin2": location_result["Admin2"],
                    "Province_State": location_result["Province_State"],
                    "Country_Region": location_result["Country_Region"],
                    "Lat": location_result["Lat"],
                    "Long_": location_result["Long_"],
                    "confirmed": {},
                    "deaths": {}
                }

            for date, amount in dates.items():
                location_result[location_id][stat][date] = int(amount or 0)

        return location_result

    def _location_id(self, tuple_id: tuple):
        """Generates string ID given tuple containing a variable number of fields.
        
        Arguments:
            tuple_id {tuple} -- tuple containing county, state and FIPS code.
        
        Returns:
            str -- string ID representation.
        """
        return "@".join([item for item in tuple_id])

    def _get_field_from_map(self, data, field) -> str:  # TODO: Extract to utils
        """Tries to get value from a map by key. Otherwise, returns empty string.

        Arguments:
            data {map} -- the map to query.
            field {str} -- the field we want to get.

        Returns:
            str -- string value at field.
        """
        return data[field] if field in data else ""

    def _filter_date_columns(self, items):
        return dict(
            filter(
                lambda element: self._valid_date(self._valid_date(element[0]))
            ),
            items
        )

    def _valid_date(self, date: str, fuzzy: bool = False) -> bool: # TODO: Move to util
        try:
            parse(date, fuzzy=fuzzy)
            return True
        except ValueError:
            return False
