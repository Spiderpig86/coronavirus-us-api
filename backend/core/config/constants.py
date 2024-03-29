"""Application Constants

All of the application constants can be found here.
"""
import os
from urllib.parse import urlparse

from pydantic import AnyUrl

from .config import CONFIG

# App
APP_VERSION = "1.0.0"
APP_NAME = "coronavirus-us-api"
APP_DESCRIPTION = (
    "API is designed to serve up to date US Coronavirus statistics in the United States. "
    "Find it at: [Github](https://github.com/Spiderpig86/coronavirus-us-api)"
)
APP_DEBUG = CONFIG.get("fastapi.debug")

# API Tags
API_PREFIX = "/api"
API_TAG_HEALTH = "health"
API_TAG_DATA = "data"
API_TAG_COUNTY = "county"
API_TAG_STATE = "state"
API_TAG_COUNTRY = "country"

# Configuration
CONFIG_PATH = "config/config.yml"
CONFIG_APP_HOST: str = CONFIG.get("app.host")
CONFIG_APP_PORT: str = CONFIG.get("app.port")
CONFIG_APP_LOG_LEVEL: str = CONFIG.get("app.log_level")

# Deployment
STAGE: str = os.environ.get("STAGE")
REDIS_URL: AnyUrl = urlparse(os.environ.get("REDISCLOUD_URL")) if os.environ.get(
    "REDISCLOUD_URL"
) else ""

REDIS_CACHE_TIMEOUT_SECONDS = 43200  # 12 hours
LOCATION_CACHE_TIMEOUT_SECONDS = 86400  # 24 hours

# Data Endpoints
DATA_ENDPOINTS = {
    "NytFacade__Counties": "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv",
    "NytFacade__States": "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv",
    "NytFacade__Country": "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv",
    "JhuFacade": "https://raw.githubusercontent.com/CSSEGISandData/2019-nCoV/master/csse_covid_19_data/csse_covid_19_time_series",
    "LocationDataService": "https://raw.githubusercontent.com/Spiderpig86/coronavirus-us-api/master/data/",
}

# API Metadata
TAGS_METADATA = [
    {"name": "health", "description": "API for checking service health."},
    {
        "name": "county",
        "description": "Statistics for locations on the **county** level.",
    },
    {
        "name": "state",
        "description": "Statistics for locations on the **state** level.",
    },
    {
        "name": "country",
        "description": "Statistics for locations on the **country** level.",
    },
    {"name": "data", "description": "Endpoint to show available data sources."},
]
