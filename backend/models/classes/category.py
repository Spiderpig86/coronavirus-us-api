"""Category

Concrete impelementation of Category model which contains historical data for a category at a given location
"""
from collections import OrderedDict


class Category:
    def __init__(self, history=None):
        self.__category = history if history else {}

    @property
    def category(self):
        """Retrieves historical data for category sorted by date.
        
        Returns:
            {OrderedDict} -- dictionary holding chronological stats.
        """
        return OrderedDict(sorted(self.__category.items()))

    @property
    def latest(self):
        """Extracts latest value from history.
        
        Returns:
            {int} -- latest statistic for given category and location.
        """
        values = list(self.category.values())

        if values:
            return values[-1] or 0

        # Fallback value of 0.
        return 0

    @property
    def sum(self):
        """Gets the numerical sum of statistic for category.
        
        Returns:
            {int} -- sum for statistic.
        """

        values = list(self.category.values())
        return sum(values)

    def to_dict(self):
        """Transforms Category to dict representation.
        
        Returns:
            {dict} -- dictionary representation of Category.
        """
        return {"latest": self.latest, "history": self.category}
