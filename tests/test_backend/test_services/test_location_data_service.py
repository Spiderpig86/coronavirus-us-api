import json
import os
from unittest import mock

import pytest

from backend.core.config.constants import DATA_ENDPOINTS
from backend.models.classes.category import Category
from backend.models.classes.coordinates import Coordinates
from backend.models.classes.location_properties import LocationProperties
from backend.services.location_data_service import LocationDataService
from backend.utils.country_population import COUNTRY_POPULATION
from tests.base_test import TestBase
from tests.conftest import mocked_strptime_isoformat

EXPECTED_COUNTRY_DATA = {
    "UID": "840",
    "iso2": "US",
    "iso3": "USA",
    "code3": "840",
    "fips": "",
    "county": "",
    "state": "",
    "country": "US",
    "coordinates": Coordinates("37.0902", "-95.7129").to_dict(),
    "combined_key": "United States",
    "population": COUNTRY_POPULATION["US"],
}

EXPECTED_STATE_DATA = {
    "UID": "84000053",
    "iso2": "US",
    "iso3": "USA",
    "code3": "840",
    "fips": "53",
    "county": "",
    "state": "Washington",
    "country": "US",
    "coordinates": Coordinates("47.4009", "-121.4905").to_dict(),
    "combined_key": "Washington, US",
    "population": 7614893,
}

EXPECTED_COUNTY_DATA = {
    "UID": "84053033",
    "iso2": "US",
    "iso3": "USA",
    "code3": "840",
    "fips": "53033",
    "county": "King",
    "state": "Washington",
    "country": "US",
    "coordinates": Coordinates("47.49137892", "-121.8346131").to_dict(),
    "combined_key": "King, Washington, US",
    "population": 2252782,
}


@pytest.mark.asyncio
async def test_get_country_data(mock_web_client):
    # Act
    result = await LocationDataService().get_country_data()

    # Assert
    assert ("US",) in result
    assert result[("US",)].to_dict() == EXPECTED_COUNTRY_DATA


@pytest.mark.asyncio
async def test_get_state_data(mock_web_client):
    # Act
    result = await LocationDataService().get_state_data()

    # Assert
    assert ("US", "Washington") in result
    assert result[("US", "Washington")].to_dict() == EXPECTED_STATE_DATA


@pytest.mark.asyncio
async def test_get_county_data(mock_web_client):
    # Act
    result = await LocationDataService().get_county_data()

    # Assert
    assert ("US", "Washington", "king") in result
    assert result[("US", "Washington", "king")].to_dict() == EXPECTED_COUNTY_DATA
