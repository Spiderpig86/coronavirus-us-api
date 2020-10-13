"""New York Times Information Retriever

Fetches live information for Coronanvirus statistics from the New York Times.
Data is regularly updated here: https://github.com/nytimes/covid-19-data
"""
import csv
import time
from datetime import datetime, timedelta
from typing import List

from asyncache import cached
from cachetools import TTLCache
from loguru import logger

from backend.core.libs import webclient
from backend.models.classes.category import Category
from backend.models.classes.location import NytLocation
from backend.models.classes.statistics import Statistics
from backend.models.swagger.history import Timelines
from backend.utils.functions import Functions


class NytDataService(object):
    @cached(cache=TTLCache(maxsize=128, ttl=3600))
    async def get_data(self, endpoint: str, cache_tag: str = ""):
        """Method that retrieves data from the New York Times.
        
        Arguments:
            endpoint {str} -- string that represents endpoint to get data from.

        Returns:
            Location[], str -- returns list of location stats and the last updated date.
        """
        from backend.utils.containers import Container

        _start = time.time() * 1000.0
        grouped_locations, from_cache = await self._group_locations_wrapper(
            endpoint, cache_tag
        )
        _end = time.time() * 1000.0
        logger.info(f"Elapsed grouped_locations {str(_end-_start)}ms")

        locations = []
        last_updated = Functions.get_formatted_date()
        to_serialize = {"locations": {}}  # For cache

        _start = time.time() * 1000.0
        for location_id, events in grouped_locations.items():
            confirmed_map = events["confirmed"]
            deaths_map = events["deaths"]

            confirmed = Category(confirmed_map)
            deaths = Category(deaths_map)

            locations.append(
                NytLocation(
                    id=location_id,
                    country=events["country"],
                    county=events["county"],
                    state=events["state"],
                    fips=events["fips"],
                    timelines={"confirmed": confirmed, "deaths": deaths,},
                    last_updated=last_updated,
                    latest=Statistics(
                        confirmed=confirmed.latest, deaths=deaths.latest
                    ).to_dict(),
                )
            )
            # Transform to store in cache
            # Track the first date with new object entry
            if not from_cache:
                to_serialize["locations"][location_id] = {
                    **grouped_locations[location_id]
                }
                to_serialize["locations"][location_id][
                    "first_date"
                ] = Functions.get_formatted_date(next(iter(confirmed_map)), "%Y-%m-%d")
                to_serialize["locations"][location_id]["confirmed"] = list(
                    confirmed_map.values()
                )
                to_serialize["locations"][location_id]["deaths"] = list(
                    deaths_map.values()
                )

        if not from_cache:
            await Container.cache().set_item(f"nyt_data_{cache_tag}", to_serialize)

        _end = time.time() * 1000.0
        logger.info(f"Elapsed loop {str(_end-_start)}ms")

        logger.info("Finished transforming NYT results.")
        return locations, last_updated

    async def _group_locations_wrapper(self, endpoint: str, cache_tag: str):
        """Function wrapping _group_locations to handle caching.

        Arguments:
            endpoint {str} -- endpoint of data.
            cache_tag {str} -- identifier for cache data for NYT.

        Returns:
            (dict, bool) -- returns a dictionary of aggregated locations and a boolean indicating if data was from cache.
        """
        from backend.utils.containers import Container

        # Check for cached results
        cache_result = (
            await Container.cache().get_item(f"nyt_data_{cache_tag}")
            if cache_tag
            else None
        )
        if cache_result:
            result = {}
            keys = list(cache_result["locations"].keys())

            for location in keys:
                confirmed_map, deaths_map = {}, {}
                date = datetime.strptime(
                    Functions.get_formatted_date(
                        cache_result["locations"][location]["first_date"]
                    ),
                    "%Y-%m-%d",
                )  # Pop the date key out of the object

                for confirmed, deaths in zip(
                    cache_result["locations"][location]["confirmed"],
                    cache_result["locations"][location]["deaths"],
                ):
                    formatted_date = Functions.to_format_date(date)
                    confirmed_map[formatted_date] = int(confirmed or 0)
                    deaths_map[formatted_date] = int(deaths or 0)

                    date += timedelta(days=1)

                # Clone results to new dict
                result[location] = {**cache_result["locations"][location]}
                result[location]["confirmed"] = confirmed_map
                result[location]["deaths"] = deaths_map

            return result, True

        csv_data = ""
        logger.info("Fetching NYT data...")

        # https://docs.aiohttp.org/en/stable/client_quickstart.html#make-a-request
        async with webclient.WEBCLIENT.get(endpoint) as response:
            csv_data = await response.text()

        parsed_data = list(csv.DictReader(csv_data.splitlines()))
        return self._group_locations(parsed_data), False

    def _group_locations(self, csv_data: List):
        """Groups statistics by given county and state.
        
        Arguments:
            csv_data {List} -- list containing every row result in NYT data.
        
        Returns:
            {Dict} -- dictionary containing timeseries for confirmed cases and deaths grouped by location.
        """
        location_result = {}
        for timestamp in csv_data:
            # location_id = (
            #     "US",
            #     self._get_field_from_map(timestamp, "state"),
            #     self._get_field_from_map(timestamp, "county"),
            #     self._get_field_from_map(timestamp, "fips") or "0", # Edge case when NYT does not have FIPS
            # )
            state = self._get_field_from_map(timestamp, "state")
            county = self._get_field_from_map(timestamp, "county")
            fips = self._get_field_from_map(timestamp, "fips")
            location_id = "US"

            if state:
                location_id += f"@{state}"
            if county:
                location_id += f"@{county}"
            if fips:
                location_id += f"@{fips}"

            updated_date = Functions.get_formatted_date(timestamp["date"], "%Y-%m-%d")
            confirmed = timestamp["cases"]
            deaths = timestamp["deaths"]

            if location_id not in location_result:
                location_result[location_id] = {
                    "confirmed": {},
                    "deaths": {},
                    "country": "US",
                    "state": state,
                    "county": county,
                    "fips": fips,
                }

            # Collect stats from the same location
            location_result[location_id]["confirmed"][updated_date] = int(
                confirmed or 0
            )
            location_result[location_id]["deaths"][updated_date] = int(deaths or 0)

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
