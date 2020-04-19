"""Data Service Container

Data Service Container used for dependency injection into routes for data retrieval.
"""

from backend.services.nyt import NytService

DATA_SOURCE_CONTAINER = {"nyt": NytService()}


def get_data_source(data_source: str):
    """Retrieves a data source service given the data source alias.
    
    Arguments:
        data_source {str} -- data source alias.

        # TODO: Update pydoc
    """
    return DATA_SOURCE_CONTAINER.get(data_source.lower())
