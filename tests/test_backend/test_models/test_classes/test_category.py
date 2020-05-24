"""Category Test

Category unit test.
"""

import pytest

from collections import OrderedDict
from backend.models.classes.category import Category


TEST_CATEGORY_DATA = {
    "2020-02-01T00:00:00Z": 5,
    "2020-02-02T00:00:00Z": 6,
    "2020-02-03T00:00:00Z": 21,
    "2020-02-04T00:00:00Z": 84,
    "2020-02-05T00:00:00Z": 120,
    "2020-02-06T00:00:00Z": 158
}

def test__empty_category__success():
    # Arrange
    category = Category()

    # Act and Assert
    assert category.category != None
    assert len(category.category) == 0
    assert category.latest == 0

    expected_dict = {
        "latest": 0,
        "history": OrderedDict()
    }
    assert category.to_dict() == expected_dict
    
def test__valid_category__success():
    # Arrange
    category = Category(TEST_CATEGORY_DATA)

    # Act and Assert
    assert category.category != None
    assert len(category.category) == 6
    assert category.latest == 158

    expected_dict = {
        "latest": 158,
        "history": OrderedDict([("2020-02-01T00:00:00Z", 5), ("2020-02-02T00:00:00Z", 6), ("2020-02-03T00:00:00Z", 21), ("2020-02-04T00:00:00Z", 84), ("2020-02-05T00:00:00Z", 120), ("2020-02-06T00:00:00Z", 158)])
    }
    assert category.to_dict() == expected_dict