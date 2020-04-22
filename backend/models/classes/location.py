"""Location Implementation

Concrete implementation of the Location model.
"""


class Location:
    def __init__(self, id, country, state, county, fips, history, last_updated, latest):
        self.id = id
        self.country = country
        self.state = state
        self.county = county
        self.fips = fips
        self.history = history
        self.last_updated = last_updated
        self.latest = latest

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
        # TODO: Implement
        return -1

    def to_dict(self, include_timelines=False):
        """Transforms location model to dictionary representation.
        
        Keyword Arguments:
            include_history {bool} -- flag to toggle inclusion of historical information (default: {False})
        
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
            response["timelines"] = {k: v.to_dict() for k, v in self.history.items()}

        return response
