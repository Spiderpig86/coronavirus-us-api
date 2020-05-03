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

# Configuration
CONFIG_PATH = "config/config.yml"
CONFIG_APP_PORT = CONFIG.get("app.port")
CONFIG_FASTAPI_DEBUG_KEY = "debug"

# Data Endpoints
DATA_ENDPOINTS = {
    "NytDataService": "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv",
    "LocationStatsService": "localhost:8000",
}
