"""Facade

Abstract class to represent responsibilities of facades.
"""
from abc import ABC, abstractmethod


class AbstractDataSourceFacade(ABC):
    @abstractmethod
    def get_state_data(self):
        """Method for retrieving virus statistics on state level.

        Raises:
            NotImplementedError: Exception will be thrown for unimplemented method stub.
        """
        raise NotImplementedError

    @abstractmethod
    def get_county_data(self):
        """Method for retrieving virus statistics on county level.

        Raises:
            NotImplementedError: Exception will be thrown for unimpelemented method stub.
        """
        raise NotImplementedError
