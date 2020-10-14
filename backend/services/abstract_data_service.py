"""Facade

Abstract class to represent responsibilities of data service for Covid data.
"""
from abc import ABC, abstractmethod


class AbstractDataService(ABC):
    @abstractmethod
    def get_data(self, endpoint: str, data_type: str = ''):
        """Function for retrieving data for a given endpoint.

        Arguments:
            endpoint {str} -- endpoint where the data resides.
            data_type {str} -- name to classify what the data is.
        """
        raise NotImplementedError
