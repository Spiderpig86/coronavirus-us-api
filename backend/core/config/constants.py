"""Application Constants

All of the application constants can be found here.
"""
from .config import CONFIG

# App
APP_VERSION = "0.0.1"
APP_NAME = "covid-us-api"
APP_DESCRIPTION = (
    "API is designed to serve up to date US Coronavirus statistics in the United States. "
    "Find it at: https://github.com/Spiderpig86/coronavirus-us-api"
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
CONFIG_APP_HOST = CONFIG.get("app.host")
CONFIG_APP_PORT = CONFIG.get("app.port")
CONFIG_APP_LOG_LEVEL = CONFIG.get("app.log_level")
CONFIG_FASTAPI_DEBUG_KEY = "debug"

# Data Endpoints
DATA_ENDPOINTS = {
    "NytFacade__Counties": "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv",
    "NytFacade__States": "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv",
    "NytFacade__Country": "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv",
    "JhuFacade": "https://raw.githubusercontent.com/CSSEGISandData/2019-nCoV/master/csse_covid_19_data/csse_covid_19_time_series",
    "LocationDataService": "https://raw.githubusercontent.com/Spiderpig86/coronavirus-us-api/master/data/",
}
