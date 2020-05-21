"""Functions.py Tests

Tests for functions class.
Test files follow this convention: https://osherove.com/blog/2005/4/3/naming-standards-for-unit-tests.html
"""
from datetime import datetime
from unittest import mock

import pytest

from backend.utils.functions import Functions

TEST_DATETIME = datetime(2020, 5, 21, 0, 0, 0)


@pytest.mark.parametrize(
    "initial_date, format, expected_value",
    [
        ("05/18/20", "%m/%d/%y", "2020-05-18T00:00:00Z"),
        ("2020-05-18", "%Y-%m-%d", "2020-05-18T00:00:00Z"),
    ],
)
def test__get_formatted_date__given_valid_parameters__success(
    initial_date, format, expected_value
):
    assert Functions.get_formatted_date(initial_date, format) == expected_value


def test__get_formatted_date__given_no_parameters__success():
    result = None
    with mock.patch("backend.utils.functions.datetime") as mock_datetime:
        mock_datetime.utcnow.return_value = TEST_DATETIME
        result = Functions.get_formatted_date()

    assert result == "2020-05-21T00:00:00Z"


def test__get_formatted_date__given_empty_initial_date__success():
    result = None
    with mock.patch("backend.utils.functions.datetime") as mock_datetime:
        mock_datetime.utcnow.return_value = TEST_DATETIME
        result = Functions.get_formatted_date("")

    assert result == "2020-05-21T00:00:00Z"


@pytest.mark.parametrize(
    "initial_date, format", [("2020-05-21", "%Y/%m/%d"), ("eeee", "aaaa"),],
)
def test__get_formatted_date__given_valid_parameters__error(initial_date, format):
    with pytest.raises(ValueError):
        assert Functions.get_formatted_date(initial_date, format)


# TODO: Empty tuple case
@pytest.mark.parametrize(
    "tuple_id, expected_value",
    [
        (("country",), "country"),
        (("country", "state"), "country@state"),
        (("country", "state", "county"), "country@state@county"),
    ],
)
def test__to_location_id__given_valid_parameters__success(tuple_id, expected_value):
    assert Functions.to_location_id(tuple_id) == expected_value


@pytest.mark.parametrize(
    "tuple_id", [(None), ("test")],
)
def test__to_location_id__given_invalid_parameters__error(tuple_id):
    with pytest.raises(ValueError):
        assert Functions.to_location_id(tuple_id)
