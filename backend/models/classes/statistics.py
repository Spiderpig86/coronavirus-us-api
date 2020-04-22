"""Statistics

Concrete implementation of Statistics model.
"""

class Statistics:

    def __init__(self, confirmed, deaths):
        self.confirmed = confirmed
        self.deaths = deaths

    def to_dict(self):
        return {
            'confirmed': self.confirmed,
            'deaths': self.deaths
        }