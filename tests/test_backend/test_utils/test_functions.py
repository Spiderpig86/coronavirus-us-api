"""Functions.py Tests

Tests for functions class.
Test files follow this convention: https://osherove.com/blog/2005/4/3/naming-standards-for-unit-tests.html
"""
import pytest

from backend.utils.functions import Functions


@pytest.mark.parametrize(
    "initial_date, format, expected_value",
    [
        # (None, None, ""),
        ("05/18/20", "%m/%d/%y", "2020-05-18T00:00:00Z"),
        ("2020-05-18", "%Y-%m-%d", "2020-05-18T00:00:00Z"),
    ],
)
def test__get_formatted_date__given_valid_parameters__success(
    initial_date, format, expected_value
):
    assert Functions.get_formatted_date(initial_date, format) == expected_value


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
