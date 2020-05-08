"""Location Implementation

Concrete implementation of the Location model.
"""
from backend.utils.country_population import COUNTRY_POPULATION

class Location:
    def __init__(
        self, id, country, state, county, fips, timelines, last_updated, latest
    ):
        self.id = id
        self.country = country
        self.state = state
        self.county = county
        self.fips = fips
        self.timelines = timelines
        self.last_updated = last_updated
        self.latest = latest
        self.properties = None # This is set later

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

    def to_dict(self, include_timelines=False):
        """Transforms location model to dictionary representation.
        
        Keyword Arguments:
            include_timelines {bool} -- flag to toggle inclusion of historical information (default: {False})
        
        Returns:
            {dict} -- dictionary representation of Location class.
        """

        response = {
            "id": self.id,
            "country": self.country,
            "state": self.state,
            "county": self.county,
            "fips": self.fips,
            "last_updated": self.last_updated,
            "latest": self.latest,
            # Properties
            "state_population": self.state_population,
            "country_population": self.country_population,
        }

        if include_timelines:
            response["timelines"] = {k: v.to_dict() for k, v in self.timelines.items()}

        return response
