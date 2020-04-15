"""New York Times Information Retriever

Fetches live information for Coronanvirus statistics from the New York Times.
Data is regularly updated here: https://github.com/nytimes/covid-19-data
"""
import csv

from asyncache import cached
from cachetools import TTLCache

from backend.core.config.constants import DATA_ENDPOINTS
from backend.core.utils.webclient import WEBCLIENT


class NytService:
    def __init__(self):
        self.ENDPOINT = DATA_ENDPOINTS.get(type(self).__name__)

    @cached(cache=TTLCache(maxsize=1024, ttl=3600))
    async def get_data():
        csv_data = ""

        # https://docs.aiohttp.org/en/stable/client_quickstart.html#make-a-request
        async with WEBCLIENT.get(self.ENDPOINT) as response:
            csv_data = await response.text()

        parsed_data = list(csv.DictReader(csv_data.splitlines()))

    async def get_reduced_data():
        pass
