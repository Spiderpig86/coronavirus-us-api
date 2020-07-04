"""Functions

Collection of utility functions for various parts of API.
TODO: Split functions to separate files based on responsibilities.
"""
from datetime import datetime

from asyncache import cached
from cachetools import TTLCache


class Functions:
    @staticmethod
    def get_formatted_date(initial_date: str = None, format: str = "%Y-%m-%d") -> str:
        """Generates formatted date strings to be used as keys.
        Function is written this way due to unit testing.

        Keyword Arguments:
            initial_date {Date} -- datetime object to format (default: {None})
            format {Date} -- format of given date string (default: {"%Y-%m-%d"} for NYT)

        Returns:
            str -- resulting ISO format date string.
        """
        if initial_date:
            return Functions._get_formatted_date_with_param(initial_date, format)
        return datetime.utcnow().strftime("%Y-%m-%d")

    @staticmethod
    @cached(cache=TTLCache(maxsize=512, ttl=3600))
    def _get_formatted_date_with_param(initial_date: str, format: str) -> str:
        """Helper method to format dates based on given format and memoizes results.

        Arguments:
            initial_date {str} -- string representing date to format.
            format {str} -- format of the date.

        Returns:
            datetime -- datetime object of the given date parameter.
        """
        return datetime.strptime(initial_date, format).strftime("%Y-%m-%d")

    @staticmethod
    @cached(cache=TTLCache(maxsize=512, ttl=3600))
    def to_format_date(initial_date: datetime) -> str:
        return initial_date.strftime("%Y-%m-%d")

    @staticmethod
    @cached(cache=TTLCache(maxsize=512, ttl=3600))
    def to_location_id(tuple_id: tuple):
        """Generates string ID given tuple containing a variable number of fields.
        
        Arguments:
            tuple_id {tuple} -- tuple containing county, state and FIPS code.
        
        Returns:
            str -- string ID representation.
        """
        if not tuple_id:
            raise ValueError("The given 'tuple_id' cannot be null or empty.")

        if type(tuple_id) != tuple:
            raise ValueError(
                f"Given 'tuple_id' must of type tuple, but was {type(tuple_id)}."
            )

        return "@".join([item for item in tuple_id if len(item) > 0])

    @staticmethod
    @cached(cache=TTLCache(maxsize=512, ttl=3600))
    def to_location_tuple(location_id: str):
        """Generates string ID given tuple containing a variable number of fields.
        
        Arguments:
            tuple_id {tuple} -- tuple containing county, state and FIPS code.
        
        Returns:
            str -- string ID representation.
        """
        if not location_id:
            raise ValueError("The given 'location_id' cannot be null or empty.")

        if type(location_id) != str:
            raise ValueError(
                f"Given 'location_id' must of type str, but was {type(location_id)}."
            )

        return tuple(filter(lambda substring: substring, location_id.split("@")))

    @staticmethod
    def try_getattr(obj: object, attr: str):
        """Wrapper function that performs getattr(). Returns "__IGNORE__" on AttributeError.

        Arguments:
            obj {object} -- object to inspect.
            attr {str} -- attribute name to retrieve.

        Returns:
            object -- any value located at that attribute name.
        """
        try:
            return getattr(obj, attr)
        except AttributeError:
            return "__IGNORE__"
