"""Functions.py Tests

Tests for functions class.
Test files follow this convention: https://osherove.com/blog/2005/4/3/naming-standards-for-unit-tests.html
"""
from datetime import datetime
from unittest import mock

import pytest

from backend.utils.functions import Functions
from tests.base_test import MicroMock, TestBase

TEST_DATETIME = datetime(2020, 5, 21, 0, 0, 0)


@pytest.mark.parametrize(
    "initial_date, format, expected_value",
    [("05/18/20", "%m/%d/%y", "2020-05-18"), ("2020-05-18", "%Y-%m-%d", "2020-05-18"),],
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

    assert result == "2020-05-21"


def test__get_formatted_date__given_empty_initial_date__success():
    result = None
    with mock.patch("backend.utils.functions.datetime") as mock_datetime:
        mock_datetime.utcnow.return_value = TEST_DATETIME
        result = Functions.get_formatted_date("")

    assert result == "2020-05-21"


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


@pytest.mark.parametrize(
    "datetime, expected",
    [(datetime(2020, 6, 24), "2020-06-24"), (datetime(2021, 12, 21), "2021-12-21")],
)
def test__to_format_date__success(datetime, expected):
    assert Functions.to_format_date(datetime) == expected


@pytest.mark.parametrize(
    "location_id, expected",
    [
        ("US", ("US",)),
        ("US@", ("US",)),
        ("US@Washington", ("US", "Washington")),
        ("US@New York@Suffolk", ("US", "New York", "Suffolk")),
    ],
)
def test__to_location_tuple__given_valid_params__success(location_id, expected):
    assert Functions.to_location_tuple(location_id) == expected


@pytest.mark.parametrize("location_id", [(None), (dict)])
def test__to_location_tuple__given_invalid_params__error(location_id):
    with pytest.raises(ValueError):
        Functions.to_location_tuple(location_id)


@pytest.mark.parametrize(
    "obj, attr, expected",
    [(MicroMock(foo="bar"), "foo", "bar"), (MicroMock(), "yeet", "__IGNORE__")],
)
def test__try_getattr__success(obj, attr, expected):
    assert Functions.try_getattr(obj, attr) == expected
