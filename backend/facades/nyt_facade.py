"""NYT Facade

Class that interfaces with nyt_service.py to aggregate data.
"""
from backend.core.config.constants import DATA_ENDPOINTS
from backend.facades.abstract_facade import AbstractDataSourceFacade
from backend.services.nyt_service import NytDataService


class NytFacade(AbstractDataSourceFacade):
    def __init__(self):
        self.DATA_SERVICE = NytDataService()
        self.ENDPOINT = DATA_ENDPOINTS.get(self.__class__.__name__)

    async def get_country_data(self):
        ENDPOINT = DATA_ENDPOINTS.get(f"{self.__class__.__name__}__Country")
        return await self.DATA_SERVICE.get_data(ENDPOINT, "country")

    async def get_state_data(self):
        ENDPOINT = DATA_ENDPOINTS.get(f"{self.__class__.__name__}__States")
        return await self.DATA_SERVICE.get_data(ENDPOINT, "state")

    async def get_county_data(self):
        ENDPOINT = DATA_ENDPOINTS.get(f"{self.__class__.__name__}__Counties")
        return await self.DATA_SERVICE.get_data(ENDPOINT, "counties")
