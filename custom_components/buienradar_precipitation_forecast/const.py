""" buienradar precipiation forecast: constants """

# base component constants
# from custom_components.buienradar_precipitation_forecast.api import (
#     FORECAST_LEN,
#     HISTDATA_LEN,
# )


NAME = "Buienradar Precipitation Forecast"
DOMAIN = "buienradar_precipitation_forecast"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "2022.04.20"
ATTRIBUTION = "Data provided by Buienradar"
API_URL = "https://gpsgadget.buienradar.nl/data/raintext?lat=%s&lon=%s"
DEV_URL = "https://www.buienradar.nl/overbuienradar/gratis-weerdata"
ISSUE_URL = (
    "https://github.com/custom-components/buienradar_precipitation_forecast/issues"
)

# defaults
DEFAULT_NAME = NAME
DEFAULT_ICON = "mdi:weather-pouring"

# platforms
SENSOR = "sensor"
PLATFORMS = [SENSOR]

# FORECAST_SIZE = 2
# HISTDATA_SIZE = 2

# CONF_FORECAST_SIZE = "forecast_size"
# CONF_HISTDATA_SIZE = "histdata_size"

# startup message
DOMAIN_STARTUP = f"""
-------------------------------------------------------------------
Custom integration: {NAME}
Version: {VERSION}
For issues: {ISSUE_URL}
-------------------------------------------------------------------
"""
