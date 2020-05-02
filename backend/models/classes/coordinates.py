"""Coordinates

Class representing a coordinate point with latitude and longitude.
"""


class Coordinates:

    LATITUDE_KEY = "latitude"
    LONGITUDE_KEY = "longitude"

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def to_dict(self):
        """Returns dictionary representation of coordinate class.
        
        Returns:
            dict -- dictionary representation of coordinates.
        """
        return {self.LATITUDE_KEY: self.latitude, self.LONGITUDE_KEY: self.longitude}

    def __repr__(self):
        return f"[{self.LATITUDE_KEY}: {self.latitude}, {self.LONGITUDE_KEY}: {self.longitude}]"
