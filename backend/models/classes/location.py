"""Location Implementation

Concrete implementation of the Location model.
"""
from backend.utils.country_population import COUNTRY_POPULATION


class Location:
    def __init__(
        self, id, country, timelines, last_updated, latest
    ):
        self.id = id
        self.country = country.strip()
        self.timelines = timelines
        self.last_updated = last_updated
        self.latest = latest
        self.properties = None  # This is set later

    @property
    def state_population(self):
        """Returns the population of this specific state.
        
        Returns:
            int -- population of this state.
        """
        # TODO: Implement
        return -1

    @property
    def country_population(self):
        """Returns the population of the country.
        
        Returns:
            int -- population of this country.
        """
        return int(COUNTRY_POPULATION[self.country] or 0)

    def set_properties(self, properties):
        """Set location properties that include more location information.
        
        Arguments:
            properties LocationData -- location data object that holds more location information.
        """
        self.properties = properties

    def to_dict(self, include_timelines=False, properties=False):
        """Transforms location model to dictionary representation.
        
        Keyword Arguments:
            include_timelines {bool} -- flag to toggle inclusion of historical information (default: {False})
            properties {bool} -- flag to toggle inclusion of location properties (default: {False})
        
        Returns:
            {dict} -- dictionary representation of Location class.
        """

        response = {
            "id": self.id,
            "country": self.country,
            "last_updated": self.last_updated,
            "latest": self.latest,
        }

        if include_timelines:
            response["timelines"] = {k: v.to_dict() for k, v in self.timelines.items()}

        if properties:
            response["properties"] = self.properties

        return response

class NytLocation(Location):

    def __init__(self, id, country, timelines, last_updated, latest, state, county, fips):
        super().__init__(id, country, timelines, last_updated, latest)
        self.state = state
        self.county = county
        self.fips = fips

    # TODO: Update to_dict

class JhuLocation(Location):

    def __init__(self, id, country, timelines, last_updated, latest, state, uid, iso2, iso3, code3, fips, admin2, latitude, longitude):
        super().__init__(id, country, timelines, last_updated, latest)
        self.state = state
        self.uid = uid
        self.iso2 = iso2
        self.iso3 = iso3
        self.code3 = code3
        self.fips = fips
        self.admin2 = admin2
        self.latitude = latitude
        self.longitude = longitude

    # TODO: Update to_dict
