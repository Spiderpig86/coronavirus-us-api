"""New York Times Information Retriever

Fetches live information for Coronanvirus statistics from the New York Times.
Data is regularly updated here: https://github.com/nytimes/covid-19-data
"""
import csv
from datetime import datetime

from asyncache import cached
from cachetools import TTLCache

from backend.core.config.constants import DATA_ENDPOINTS
from backend.core.utils.webclient import WEBCLIENT
from backend.models.history import Category, History
from backend.models.location import Location


class NytService:
    def __init__(self):
        self.ENDPOINT = DATA_ENDPOINTS.get(type(self).__name__)

    @cached(cache=TTLCache(maxsize=1024, ttl=3600))
    async def get_data(self):
        csv_data = ""

        # https://docs.aiohttp.org/en/stable/client_quickstart.html#make-a-request
        async with WEBCLIENT.get(self.ENDPOINT) as response:
            csv_data = await response.text()

        parsed_data = list(csv.DictReader(csv_data.splitlines()))
        grouped_locations = self.group_locations(parsed_data)

        locations = []
        for location_tuple, events in grouped_locations.items():
            confirmed_map = events["confirmed"]
            deaths_map = events["deaths"]

            locations.append(
                Location(
                    id=self._location_id(location_tuple),
                    county=location_tuple[0],
                    state=location_tuple[1],
                    fips=location_tuple[2],
                    last_updated=datetime.utcnow().isoformat()
                    + "Z",  # TODO: Util function
                    history={
                        "confirmed": Category(
                            {
                                datetime.strptime(date, "%Y-%m-%d").isoformat()
                                + "Z": amount
                                for date, amount in confirmed_map.items()
                            }
                        ),
                        "deaths": Category(
                            {
                                datetime.strptime(date, "%Y-%m-%d").isoformat()
                                + "Z": amount
                                for date, amount in deaths_map.items()
                            }
                        ),
                    },
                )
            )

    async def group_locations(self, csv_data: List):
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

            if location_id not in csv_data:
                location_result[location_id] = {"confirmed": [], "deaths": []}

            # Collect stats from the same location
            location_result[location_id]["confirmed"][updated_date] = {
                "confirmed": int(confirmed or 0)
            }
            location_result[location_id]["deaths"][updated_date] = {
                "deaths": int(deaths or 0)
            }

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
