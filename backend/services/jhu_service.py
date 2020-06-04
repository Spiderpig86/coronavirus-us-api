"""Jhu Information Retriever

Fetches Coronavirus statistics updated by JHU CSSEGSI.
Data source can be found here: https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data
"""
import csv
import re
import time
from datetime import datetime
from typing import List

from asyncache import cached
from cachetools import TTLCache
from dateutil.parser import parse
from loguru import logger

from backend.core.config.constants import DATA_ENDPOINTS
from backend.core.utils import webclient
from backend.models.classes.category import Category
from backend.models.classes.location import JhuLocation
from backend.models.classes.statistics import Statistics
from backend.models.swagger.history import Timelines
from backend.utils.functions import Functions


class JhuDataService(object):
    @cached(cache=TTLCache(maxsize=1024, ttl=3600))
    async def get_data(self, endpoint: str) -> (List[JhuLocation], str):
        """Method that retrieves data from JHU CSSEGSI.
        
        Arguments:
            endpoint {str} -- string that represents endpoint to get data from.

        Returns:
            Location[], str -- returns list of location stats and the last updated date.
        """
        location_result = {}  # Store the final map of datapoints
        _start = time.time() * 1000.0
        location_result = await self._get_by_stat(
            endpoint, "confirmed", location_result
        )
        _end = time.time() * 1000.0
        logger.info(f"Elapsed grouped_locations {str(_end-_start)}ms")

        _start = time.time() * 1000.0
        location_result = await self._get_by_stat(endpoint, "deaths", location_result)
        _end = time.time() * 1000.0
        logger.info(f"Elapsed grouped_locations {str(_end-_start)}ms")

        locations = []
        last_updated = Functions.get_formatted_date()

        for location_tuple, events, in location_result.items():
            confirmed_map = events["confirmed"]
            deaths_map = events["deaths"]

            confirmed = Category(
                {
                    Functions.get_formatted_date(date, "%m/%d/%y"): amount
                    for date, amount in confirmed_map.items()
                }
            )

            deaths = Category(
                {
                    Functions.get_formatted_date(date, "%m/%d/%y"): amount
                    for date, amount in deaths_map.items()
                }
            )

            locations.append(
                JhuLocation(
                    id=Functions.to_location_id(location_tuple),
                    uid=events["UID"],
                    iso2=events["iso2"],
                    iso3=events["iso3"],
                    code3=events["code3"],
                    fips=events["FIPS"],
                    admin2=events["Admin2"],
                    state=events["Province_State"],
                    country=events["Country_Region"],
                    latitude=events["Lat"],
                    longitude=events["Long_"],
                    last_updated=last_updated,
                    timelines={"confirmed": confirmed, "deaths": deaths},
                    latest=Statistics(
                        confirmed=confirmed.latest, deaths=deaths.latest
                    ).to_dict(),
                )
            )

        logger.info("Finished transforming JHU results.")
        return locations, last_updated

    async def _get_by_stat(
        self, endpoint: str, stat: str, location_result: dict
    ):  # TODO: Change stat to enum

        # TODO: Log
        endpoint = f"{endpoint}/time_series_covid19_{stat}_US.csv"

        csv_data = ""
        logger.info("Fetching JHU data...")

        # https://docs.aiohttp.org/en/stable/client_quickstart.html#make-a-request
        async with webclient.WEBCLIENT.get(endpoint) as response:
            csv_data = await response.text()

        parsed_data = list(csv.DictReader(csv_data.splitlines()))

        for timestamp in parsed_data:
            location_id = (
                self._get_field_from_map(timestamp, "Country_Region"),
                self._get_field_from_map(timestamp, "Province_State"),
                self._get_field_from_map(timestamp, "Admin2"),
            )
            dates = self._filter_date_columns(timestamp.items())

            if location_id not in location_result:
                location_result[location_id] = {
                    "UID": self._get_field_from_map(timestamp, "UID"),
                    "iso2": self._get_field_from_map(timestamp, "iso2"),
                    "iso3": self._get_field_from_map(timestamp, "iso3"),
                    "code3": self._get_field_from_map(timestamp, "code3"),
                    "FIPS": self._get_field_from_map(timestamp, "FIPS"),
                    "Admin2": self._get_field_from_map(timestamp, "Admin2"),
                    "Province_State": self._get_field_from_map(
                        timestamp, "Province_State"
                    ),
                    "Country_Region": self._get_field_from_map(
                        timestamp, "Country_Region"
                    ),
                    "Lat": self._get_field_from_map(timestamp, "Lat"),
                    "Long_": self._get_field_from_map(timestamp, "Long_"),
                    "confirmed": {},
                    "deaths": {},
                }

            for date, amount in dates.items():
                location_result[location_id][stat][date] = int(amount or 0)

        return location_result

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
        return dict(filter(lambda element: self._valid_date(element[0]), items))

    def _valid_date(self, date: str) -> bool:  # TODO: Move to util
        # try:
        #     parse(date, fuzzy=fuzzy)
        #     return True
        # except ValueError:
        #     return False
        return re.match(r"\d+\/\d{1,2}\/\d{2}", date)
