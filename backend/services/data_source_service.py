"""Data Service Container

Data Service Container used for dependency injection into routes for data retrieval.
"""

from backend.facades.jhu_facade import JhuFacade
from backend.facades.nyt_facade import NytFacade
from backend.services.location_data_service import LocationDataService

DATA_FACADE_CONTAINER = {"nyt": NytFacade(), "jhu": JhuFacade()}
LOCATION_DATA_SERVICE = LocationDataService()


def get_data_source(data_source: str):
    """Retrieves a data source service given the data source alias.
    
    Arguments:
        data_source {str} -- data source alias.

        # TODO: Update pydoc
    """
    return DATA_FACADE_CONTAINER.get(data_source.lower())
