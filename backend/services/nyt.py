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

from backend.core.config.constants import DATA_ENDPOINTS
from backend.core.utils import webclient
from backend.models.classes.category import Category
from backend.models.classes.location import Location
from backend.models.classes.statistics import Statistics
from backend.models.history import Timelines


class NytDataService(object):
    def __init__(self):
        self.ENDPOINT = DATA_ENDPOINTS.get(self.__class__.__name__)

    @cached(cache=TTLCache(maxsize=1024, ttl=3600))
    async def get_data(self):
        csv_data = ""
        logger.info("Fetching NYT data...")

        # https://docs.aiohttp.org/en/stable/client_quickstart.html#make-a-request
        async with webclient.WEBCLIENT.get(self.ENDPOINT) as response:
            csv_data = await response.text()

        parsed_data = list(csv.DictReader(csv_data.splitlines()))

        _start = time.time() * 1000.0
        grouped_locations = self.group_locations(parsed_data)
        _end = time.time() * 1000.0
        print(f"Elapsed grouped_locations {str(_end-_start)}ms")

        locations = []
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
                Location(
                    id=self._location_id(location_tuple),
                    country="US",
                    county=location_tuple[0],
                    state=location_tuple[1],
                    fips=location_tuple[2],
                    timelines={"confirmed": confirmed, "deaths": deaths,},
                    last_updated=datetime.utcnow().isoformat()
                    + "Z",  # TODO: Util function,
                    latest=Statistics(
                        confirmed=confirmed.latest, deaths=deaths.latest
                    ).to_dict(),
                )
            )

        _end = time.time() * 1000.0
        print(f"Elapsed loop {str(_end-_start)}ms")

        logger.info("Finished transforming results.")
        return locations

    def group_locations(self, csv_data: List):
        """Groups statistics by given county and state.
        
        Arguments:
            csv_data {List} -- list containing every row result in NYT data.
        
        Returns:
            {Dict} -- dictionary containing timeseries for confirmed cases and deaths grouped by location.
        """

        location_result = {}

        for timestamp in csv_data:
            location_id = (timestamp["county"], timestamp["state"], timestamp["fips"])

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

    def _location_id(
        self, tuple_id: tuple
    ):  # TODO: Refactor to util function for multi-field id
        """Generates string ID given tuple containing county, state and FIPS code.
        
        Arguments:
            tuple_id {tuple} -- tuple containing county, state and FIPS code.
        
        Returns:
            str -- string ID representation.
        """
        return f"{tuple_id[0]}@{tuple_id[1]}@{tuple_id[2]}"
