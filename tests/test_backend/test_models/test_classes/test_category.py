"""Category Test

Category unit test.
"""

from collections import OrderedDict

import pytest

from backend.models.classes.category import Category

TEST_CATEGORY_DATA = {
    "2020-02-01": 5,
    "2020-02-02": 6,
    "2020-02-03": 21,
    "2020-02-04": 84,
    "2020-02-05": 120,
    "2020-02-06": 158,
}


def test__empty_category__success():
    # Arrange
    category = Category()

    # Act and Assert
    assert category.category is not None
    assert len(category.category) == 0
    assert category.latest == 0

    expected_dict = {"latest": 0, "history": OrderedDict()}
    assert category.to_dict() == expected_dict


def test__valid_category__success():
    # Arrange
    category = Category(TEST_CATEGORY_DATA)

    # Act and Assert
    assert category.category is not None
    assert len(category.category) == 6
    assert category.latest == 158

    expected_dict = {
        "latest": 158,
        "history": OrderedDict(
            [
                ("2020-02-01", 5),
                ("2020-02-02", 6),
                ("2020-02-03", 21),
                ("2020-02-04", 84),
                ("2020-02-05", 120),
                ("2020-02-06", 158),
            ]
        ),
    }
    assert category.to_dict() == expected_dict
