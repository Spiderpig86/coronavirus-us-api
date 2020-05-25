"""Functions

Collection of utility functions for various parts of API.
TODO: Split functions to separate files based on responsibilities.
"""
from datetime import datetime


class Functions:
    @staticmethod
    def get_formatted_date(initial_date: str = None, format: str = None) -> str:
        """Generates formatted date strings to be used as keys.

        Keyword Arguments:
            initial_date {Date} -- datetime object to format (default: {None})
            format {Date} -- format of given date string (default: {None})

        Returns:
            str -- resulting ISO format date string.
        """
        date = (
            datetime.strptime(initial_date, format)
            if initial_date
            else datetime.utcnow()
        )
        return date.isoformat() + "Z"

    @staticmethod
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
