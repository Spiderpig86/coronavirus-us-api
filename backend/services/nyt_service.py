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
from backend.services.abstract_data_service import AbstractDataService
from backend.utils.function_timer import async_timed, timed
from backend.utils.functions import Functions


class NytDataService(AbstractDataService):
    @cached(cache=TTLCache(maxsize=128, ttl=3600))
    async def get_data(self, endpoint: str, data_type: str = ""):
        """Method that retrieves data from the New York Times. It:
            - Gets all the data aggregated by location_id (state, county, fips) from cache or from source.
            - Builds result as a list so it can be consumed, will store this data if it is new.
        
        Arguments:
            endpoint {str} -- string that represents endpoint to get data from.

        Keyword Arguments:
            data_type {str} -- [description] (default: {''})

        Returns:
            Location[], str -- returns list of location stats and the last updated date.
        """
        from backend.utils.containers import Container

        # Aggregate data by location. Will check for data in cache before checking from source.
        grouped_locations, from_cache = await self._group_locations_cached(
            endpoint, data_type
        )

        # Build our result from dictionary of aggregated data
        last_updated = Functions.get_formatted_date()
        locations = await self._build_results_cached(
            grouped_locations, data_type, last_updated, from_cache
        )

        logger.info("Finished transforming NYT results.")
        return locations, last_updated

    @async_timed(description="Elapsed time for _group_locations_wrapper")
    async def _group_locations_cached(self, endpoint: str, cache_tag: str) -> dict:
        """Function wrapping _group_locations to handle caching.

        Arguments:
            endpoint {str} -- endpoint of data.
            cache_tag {str} -- identifier for cache data for NYT.

        Returns:
            (dict, bool) -- returns a dictionary of aggregated locations and a boolean indicating if data was from cache.
        """
        from backend.utils.containers import Container

        # Check for cached results
        cached_result = await Container.cache().get_item(f"nyt_data_{cache_tag}")
        if cached_result:
            return self._deserialize_data(cached_result), True

        csv_data = ""
        logger.info("Fetching NYT data...")

        # https://docs.aiohttp.org/en/stable/client_quickstart.html#make-a-request

        async with webclient.WEBCLIENT.get(endpoint) as response:
            csv_data = await response.text()

        parsed_data = csv.DictReader(csv_data.splitlines())
        return self._group_locations(parsed_data), False

    def _group_locations(self, csv_data: List) -> dict:
        """Groups statistics by given county and state.
        
        Arguments:
            csv_data {List} -- list containing every row result in NYT data.
        
        Returns:
            {Dict} -- dictionary containing timeseries for confirmed cases and deaths grouped by location.
        """
        location_result = {}
        for timestamp in csv_data:
            state = self._get_field_from_map(timestamp, "state")
            county = self._get_field_from_map(timestamp, "county")
            fips = self._get_field_from_map(timestamp, "fips")

            location_id = "US"
            for partial_key in [state, county, fips]:
                if partial_key:
                    location_id += f"@{partial_key}"

            updated_date = timestamp["date"]  # No need to format NYT dates
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

    @async_timed(description="Elapsed time for _build_results_cached")
    async def _build_results_cached(
        self,
        grouped_locations: dict,
        data_type: str,
        last_updated: str,
        from_cache: bool,
    ):
        """Given a dictionary of data aggregated by location_id, build each entry into an NytLocation object and build a serialized version of it for caching.

        Arguments:
            grouped_locations {dict} -- dictionary of data aggregated by location_id.
            data_type {str} -- category of data we retrieved from Nyt (country, state, county)
            last_updated {str} -- date the information was last updated.
            from_cache {bool} -- if the dictionary of aggregated data received was from cache.
        """

        from backend.utils.containers import Container

        locations = []
        to_serialize = {"locations": {}}

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
            if not from_cache:
                to_serialize["locations"][location_id] = self._serialize_entry(
                    location_id, grouped_locations, confirmed_map, deaths_map
                )

        if not from_cache:
            await Container.cache().set_item(f"nyt_data_{data_type}", to_serialize)

        return locations

    def _serialize_entry(
        self,
        location_id: str,
        grouped_locations: object,
        confirmed_map: dict,
        deaths_map: dict,
    ) -> dict:
        """Serializes entry into a dictionary that can be serialized as a JSON object. Used for caching.

        Arguments:
            location_id {str} -- location id of the entry.
            grouped_locations {object} -- unserialized entry for this location.
            confirmed_map {dict} -- map containing timestamps for confirmed cases.
            deaths_map {dict} -- map containing timestamps for deaths.

        Returns:
            dict -- serialized version of this location entry.
        """
        return {
            **grouped_locations[location_id],
            "first_date": Functions.get_formatted_date(
                next(iter(confirmed_map)), "%Y-%m-%d"
            ),
            "confirmed": list(confirmed_map.values()),
            "deaths": list(deaths_map.values()),
        }

    def _deserialize_data(self, cached_result: dict) -> object:
        """Deserializes the data stored in cache.

        Arguments:
            cached_result {dict} -- serialized version of data.

        Returns:
            object -- deserialized data.
        """
        result = {}
        keys = list(cached_result["locations"].keys())

        for location in keys:
            confirmed_map, deaths_map = {}, {}
            date = datetime.strptime(
                Functions.get_formatted_date(
                    cached_result["locations"][location]["first_date"]
                ),
                "%Y-%m-%d",
            )  # Pop the date key out of the object

            for confirmed, deaths in zip(
                cached_result["locations"][location]["confirmed"],
                cached_result["locations"][location]["deaths"],
            ):
                formatted_date = str(date)[
                    :10
                ]  # Quick way to convert to bypass calling strftime
                confirmed_map[formatted_date] = int(confirmed or 0)
                deaths_map[formatted_date] = int(deaths or 0)

                date += timedelta(days=1)

            # Clone results to new dict
            result[location] = {**cached_result["locations"][location]}
            result[location]["confirmed"] = confirmed_map
            result[location]["deaths"] = deaths_map

        return result

    def _get_field_from_map(self, data, field) -> str:  # TODO: Extract to utils
        """Tries to get value from a map by key. Otherwise, returns empty string.

        Arguments:
            data {map} -- the map to query.
            field {str} -- the field we want to get.

        Returns:
            str -- string value at field.
        """
        return data[field] if field in data else ""
