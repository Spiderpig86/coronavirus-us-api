"""County

Concrete implementation of County model.
"""
from dataclasses import dataclass

from backend.models.classes.coordinates import Coordinates


@dataclass
class LocationProperties(object):
    UID: str = None
    iso2: str = None
    iso3: str = None
    code3: str = None
    fips: str = None
    admin2: str = None
    state: str = None
    country: str = None
    coordinates: Coordinates = Coordinates(None, None)
    combined_key: str = None
    population: int = 0

    @staticmethod
    def build_coordinates(latitude, longitude) -> Coordinates:
        """Constructors Coordinate class given latitude and longitude
        
        Arguments:
            latitude {str} -- latitude value.
            longitude {str} -- longitude value.
        
        Returns:
            Coordinates -- object representing coordinates for location.
        """
        return Coordinates(latitude, longitude)

    def to_dict(self):
        return {
            "UID": self.UID,
            "iso2": self.iso2,
            "iso3": self.iso3,
            "code3": self.code3,
            "fips": self.fips,
            "county": self.admin2,
            "state": self.state,
            "country": self.country,
            "coordinates": self.coordinates.to_dict(),
            "combined_key": self.combined_key,
            "population": self.population,
        }
