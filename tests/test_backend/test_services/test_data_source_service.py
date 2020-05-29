"""Data Source Service Test

Data Source Service unit test.
"""
import pytest

from backend.services.data_source_service import get_data_source


@pytest.mark.parametrize(
    "data_source, expected_value", [("nyt", "NytFacade"), ("jhu", "JhuFacade"),],
)
def test__given_valid_data_source__get_data_source__success(
    data_source, expected_value
):
    source = get_data_source(data_source)
    assert source.__class__.__name__ == expected_value


@pytest.mark.parametrize(
    "data_source", [("blah"),],
)
def test__given_invalid_data_source__get_data_source__error(data_source):
    assert get_data_source(data_source) is None
