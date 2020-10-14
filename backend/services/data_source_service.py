"""Data Service Container

Data Service Container used for dependency injection into routes for data retrieval.
"""

from backend.facades.abstract_facade import AbstractDataSourceFacade
from backend.facades.jhu_facade import JhuFacade
from backend.facades.nyt_facade import NytFacade
from backend.services.location_data_service import LocationDataService


class DataSources:
    def __init__(self):
        self.DATA_FACADE_CONTAINER = {"nyt": NytFacade(), "jhu": JhuFacade()}

    def get_data_source(self, data_source: str) -> AbstractDataSourceFacade:
        """Retrieves a data source service given the data source alias.
        
        Arguments:
            data_source {str} -- data source alias.

        Returns:
            DataSourceFacade -- corresponding DataSourceFacade given parameter.
        """
        return self.DATA_FACADE_CONTAINER.get(data_source.lower())
