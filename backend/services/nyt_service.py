"""New York Times Information Retriever

Fetches live information for Coronanvirus statistics from the New York Times.
Data is regularly updated here: https://github.com/nytimes/covid-19-data
"""
import csv
import time
from datetime import datetime
from typing import List

from asyncache import cached
from cachetools import TTLCache
from loguru import logger

from backend.core.utils import webclient
from backend.models.classes.category import Category
from backend.models.classes.location import NytLocation
from backend.models.classes.statistics import Statistics
from backend.models.history import Timelines


class NytDataService(object):
    @cached(cache=TTLCache(maxsize=1024, ttl=3600))
    async def get_data(self, endpoint: str):
        """Method that retrieves data from the New York Times.
        
        Arguments:
            endpoint {str} -- string that represents endpoint to get data from.

        Returns:
            Location[], str -- returns list of location stats and the last updated date.
        """
        csv_data = ""
        logger.info("Fetching NYT data...")

        # https://docs.aiohttp.org/en/stable/client_quickstart.html#make-a-request
        async with webclient.WEBCLIENT.get(endpoint) as response:
            csv_data = await response.text()

        parsed_data = list(csv.DictReader(csv_data.splitlines()))

        _start = time.time() * 1000.0
        grouped_locations = self._group_locations(parsed_data)
        _end = time.time() * 1000.0
        logger.info(f"Elapsed grouped_locations {str(_end-_start)}ms")

        locations = []
        last_updated = datetime.utcnow().isoformat() + "Z"  # TODO: Util function
        _start = time.time() * 1000.0
        for location_tuple, events in grouped_locations.items():
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
                NytLocation(
                    id=self._location_id(location_tuple),
                    country="US",
                    county=location_tuple[0],
                    state=location_tuple[1],
                    fips=location_tuple[2],
                    timelines={"confirmed": confirmed, "deaths": deaths,},
                    last_updated=last_updated,
                    latest=Statistics(
                        confirmed=confirmed.latest, deaths=deaths.latest
                    ).to_dict(),
                )
            )

        _end = time.time() * 1000.0
        logger.info(f"Elapsed loop {str(_end-_start)}ms")

        logger.info("Finished transforming NYT results.")
        return locations, last_updated

    def _group_locations(self, csv_data: List):
        """Groups statistics by given county and state.
        
        Arguments:
            csv_data {List} -- list containing every row result in NYT data.
        
        Returns:
            {Dict} -- dictionary containing timeseries for confirmed cases and deaths grouped by location.
        """
        location_result = {}

        for timestamp in csv_data:
            location_id = (
                self._get_field_from_map(timestamp, "county"),
                self._get_field_from_map(timestamp, "state"),
                self._get_field_from_map(timestamp, "fips"),
            )

            updated_date = timestamp["date"]
            confirmed = timestamp["cases"]
            deaths = timestamp["deaths"]

            if location_id not in location_result:
                location_result[location_id] = {"confirmed": {}, "deaths": {}}

            # Collect stats from the same location
            location_result[location_id]["confirmed"][updated_date] = int(
                confirmed or 0
            )
            location_result[location_id]["deaths"][updated_date] = int(deaths or 0)
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
