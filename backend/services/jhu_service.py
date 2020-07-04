"""Jhu Information Retriever

Fetches Coronavirus statistics updated by JHU CSSEGSI.
Data source can be found here: https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data
"""
import asyncio
import csv
import json
import re
import time
from datetime import datetime, timedelta
from typing import List, Tuple

from asyncache import cached
from cachetools import TTLCache
from dateutil.parser import parse
from loguru import logger

from backend.core.config.constants import DATA_ENDPOINTS
from backend.core.libs import webclient
from backend.models.classes.category import Category
from backend.models.classes.location import JhuLocation
from backend.models.classes.statistics import Statistics
from backend.models.swagger.history import Timelines
from backend.utils.functions import Functions


class JhuDataService(object):
    @cached(cache=TTLCache(maxsize=512, ttl=3600))
    async def get_data(self, endpoint: str) -> (List[JhuLocation], str):
        """Method that retrieves data from JHU CSSEGSI.
        
        Arguments:
            endpoint {str} -- string that represents endpoint to get data from.

        Returns:
            Location[], str -- returns list of location stats and the last updated date.
        """
        _start = time.time() * 1000.0
        promises = await asyncio.gather(
            self._fetch_csv_data(endpoint, "confirmed"),
            self._fetch_csv_data(endpoint, "deaths"),
        )
        _end = time.time() * 1000.0
        logger.info(f"Elapsed _fetch_csv_data for all stats {str(_end-_start)}ms")

        _start = time.time() * 1000.0
        tagged_promises = self._tag_promised_results(
            ["confirmed", "deaths"], promises
        )  # [("confirmed", ...), ...]
        location_result = await self._zip_results(
            tagged_promises
        )  # Store the final map of datapoints { "Locations": {}, "first_date": {} }
        _end = time.time() * 1000.0
        logger.info(f"Elapsed _zip_results for all stats {str(_end-_start)}ms")

        locations = []
        last_updated = Functions.get_formatted_date()

        for location_id, events, in location_result.items():
            confirmed_map = events["confirmed"]
            deaths_map = events["deaths"]

            confirmed = Category(confirmed_map)
            deaths = Category(deaths_map)

            locations.append(
                JhuLocation(
                    id=location_id,
                    uid=events["uid"],
                    iso2=events["iso2"],
                    iso3=events["iso3"],
                    code3=events["code3"],
                    fips=events["FIPS"],
                    county=events["Admin2"],
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

    async def _fetch_csv_data(self, endpoint: str, stat: str) -> List[object]:
        # TODO: Log
        endpoint = f"{endpoint}/time_series_covid19_{stat}_US.csv"

        csv_data = ""
        logger.info(f"Fetching JHU data for {stat} stat...")

        # https://docs.aiohttp.org/en/stable/client_quickstart.html#make-a-request
        async with webclient.WEBCLIENT.get(endpoint) as response:
            csv_data = await response.text()

        parsed_data = list(csv.DictReader(csv_data.splitlines()))

        # TODO: Log
        return parsed_data

    async def _zip_results(self, data: List[Tuple]) -> dict:
        from backend.utils.containers import Container

        # First check cache
        # TODO: Refactor all of caching
        cache_result = await Container.cache().get_item(f"jhu_data")
        if cache_result:

            # Initialize copy dict and values we need
            result = {}
            first_date = datetime.strptime(
                Functions.get_formatted_date(cache_result.get("first_date")), "%Y-%m-%d"
            )  # Pop the date key out of the object
            keys = list(cache_result["locations"].keys())

            for location in keys:
                confirmed_map, deaths_map = {}, {}
                date = first_date
                i = 0

                for confirmed, deaths in zip(
                    cache_result["locations"][location]["confirmed"],
                    cache_result["locations"][location]["deaths"],
                ):
                    confirmed_map[Functions.to_format_date(date)] = int(confirmed or 0)
                    deaths_map[Functions.to_format_date(date)] = int(deaths or 0)

                    date += timedelta(days=1)
                    i += 1

                # Clone resuilts to new dict
                result[location] = {**cache_result["locations"][location]}
                result[location]["confirmed"] = confirmed_map
                result[location]["deaths"] = deaths_map

            return result

        location_result = {}
        to_serialize = {"locations": {}}
        for stat, locations in data:
            self._populate_location_result(
                stat, locations, location_result, to_serialize
            )

        await Container.cache().set_item("jhu_data", to_serialize, 300)
        return location_result

    def _populate_location_result(
        self,
        stat: str,
        locations: List[dict],
        location_result: dict,
        to_serialize: dict,
    ):
        """Populates map with information for given location with timeline data.

        Arguments:
            stat {str} -- Statistic we are populating, eg. "Confirmed".
            locations {List[dict]} -- List of maps representing location info. Here, data that does not exist is None and needs to be transformed to "".
            location_result {dict} -- Map of finalized location data to put data in.
        """

        for location in locations:
            location_tuple = (
                self._get_field_from_map(location, "Country_Region"),
                self._get_field_from_map(location, "Province_State"),
                self._get_field_from_map(location, "Admin2"),
            )
            serialized_id = Functions.to_location_id(location_tuple)
            dates = self._filter_date_columns(location.items())

            if serialized_id not in location_result:
                location_result[serialized_id] = {
                    "uid": self._get_field_from_map(location, "UID"),
                    "iso2": self._get_field_from_map(location, "iso2"),
                    "iso3": self._get_field_from_map(location, "iso3"),
                    "code3": self._get_field_from_map(location, "code3"),
                    "FIPS": self._get_field_from_map(location, "FIPS"),
                    "Admin2": self._get_field_from_map(location, "Admin2"),
                    "Province_State": self._get_field_from_map(
                        location, "Province_State"
                    ),
                    "Country_Region": self._get_field_from_map(
                        location, "Country_Region"
                    ),
                    "Lat": self._get_field_from_map(location, "Lat"),
                    "Long_": self._get_field_from_map(location, "Long_"),
                    "confirmed": {},
                    "deaths": {},
                }

                to_serialize["locations"][serialized_id] = {
                    **location_result[serialized_id],
                }

            for date, amount in dates.items():
                location_result[serialized_id][stat][
                    Functions.get_formatted_date(date, "%m/%d/%y")
                ] = int(amount or 0)

            to_serialize["locations"][serialized_id][stat] = list(
                location_result[serialized_id][stat].values()
            )

            # Track the first date with new object entry
            if "first_date" not in to_serialize:
                to_serialize["first_date"] = Functions.get_formatted_date(
                    next(iter(dates)), "%m/%d/%y"
                )

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

    def _tag_promised_results(self, tags, promises) -> List[Tuple]:
        """Associates tag with a given promised result as a pair (tuple).

        Args:
            tags (List[str]): List of strings to use for tagging.
            promises (List[object]): List of promised results to tag.

        Raises:
            Exception: Raised when given list of tags and promises are not of equal length.

        Returns:
            List: List of tag promise pairs.
        """

        if len(tags) != len(promises):
            raise ValueError("Error: len(tag) and len(promises) must be equal.")

        tagged_promises = [(tag, promise) for tag, promise in zip(tags, promises)]
        return tagged_promises

    def _serialize_locations(self, locations: List[JhuLocation]) -> List[dict]:
        """Serializes list of JhuLocations for caching.

        Arguments:
            locations {List[JhuLocation]} -- list of JhuLocation objects.

        Returns:
            List[dict] -- list of serialized locations.
        """
        return list(map(lambda location: location.to_dict(True), locations))

    def _deserialize_locations(
        self, serialized_locations: List[dict]
    ) -> List[JhuLocation]:
        """Deserializes list of dicts into JhuLocation objects.

        Arguments:
            serialized_locations {List[dict]} -- list of dicts to deserialize.

        Returns:
            List[JhuLocation] -- deserialized list of JhuLocations.
        """
        return list(
            map(
                lambda serialized_location: JhuLocation(**serialized_location),
                serialized_locations,
            )
        )
