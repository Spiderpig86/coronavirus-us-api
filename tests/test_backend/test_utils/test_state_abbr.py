"""state_abbr.py Tests

Tests for state_abbr file.
"""
import pytest

from backend.utils.state_abbr import get_state_name


@pytest.mark.parametrize(
    "code, expected_value",
    [("NY", "new york"), ("WA", "washington"), ("ca", "california"),],
)
def test__get_state_name__given_valid_parameter__success(code, expected_value):
    assert get_state_name(code) == expected_value


@pytest.mark.parametrize("code", [(None), ("XX")])
def test__get_state_name__given_invalid_parameter__error(code):
    assert get_state_name(code) == "--"
