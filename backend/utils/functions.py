"""Functions

Collection of utility functions for various parts of API.
TODO: Split functions to separate files based on responsibilities.
"""
from datetime import datetime


class Functions:
    @staticmethod
    def get_formatted_date(initial: datetime = None) -> str:
        """Generates formatted date strings to be used as keys.

        Keyword Arguments:
            initial {Date} -- datetime object to format (default: {None})

        Returns:
            str -- resulting ISO format date string.
        """
        date = datetime.strptime(initial, "%m/%d/%y") if initial else datetime.utcnow()
        return date.isoformat() + "Z"

    @staticmethod
    def to_location_id(self, tuple_id: tuple):
        """Generates string ID given tuple containing a variable number of fields.
        
        Arguments:
            tuple_id {tuple} -- tuple containing county, state and FIPS code.
        
        Returns:
            str -- string ID representation.
        """
        return "@".join([item for item in tuple_id])
