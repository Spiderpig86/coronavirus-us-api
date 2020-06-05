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
    "code3": "USA",
    "fips": "",
    "county": "",
    "state": "",
    "country": "US",
    "coordinates": Coordinates("37.0902", "-95.7129").to_dict(),
    "combined_key": "United States",
    "population": COUNTRY_POPULATION["US"],
}


@pytest.mark.asyncio
async def test_get_country_data(mock_web_client):
    result = await LocationDataService().get_country_data()

    assert ("US",) in result
    assert result[("US",)].to_dict() == EXPECTED_COUNTRY_DATA


@pytest.mark.asyncio
async def test_get_state_data(mock_web_client):
    pass


@pytest.mark.asyncio
async def test_get_county_data(mock_web_client):
    pass
