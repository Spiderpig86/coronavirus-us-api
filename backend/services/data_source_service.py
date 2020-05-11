"""Data Service Container

Data Service Container used for dependency injection into routes for data retrieval.
"""

from backend.services.jhu_service import JhuDataService
from backend.services.location_data_service import LocationDataService
from backend.services.nyt_service import NytDataService

DATA_SOURCE_CONTAINER = {"nyt": NytDataService(), "jhu": JhuDataService}
LOCATION_DATA_SERVICE = LocationDataService()


def get_data_source(data_source: str):
    """Retrieves a data source service given the data source alias.
    
    Arguments:
        data_source {str} -- data source alias.

        # TODO: Update pydoc
    """
    return DATA_SOURCE_CONTAINER.get(data_source.lower())
