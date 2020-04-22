"""Statistics

Concrete implementation of Statistics model.
"""


class Statistics:
    def __init__(self, confirmed, deaths):
        self.confirmed = confirmed
        self.deaths = deaths

    def to_dict(self):
        """Transforms Statistics to dict representation.
        
        Returns:
            {dict} -- dictionary representation of Statistics.
        """
        return {"confirmed": self.confirmed, "deaths": self.deaths}
