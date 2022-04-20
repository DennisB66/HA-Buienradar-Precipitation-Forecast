# Base component constants
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


# Defaults
DEFAULT_NAME = NAME
DEFAULT_ICON = "mdi:weather-pouring"

# Platforms
SENSOR = "sensor"
PLATFORMS = [SENSOR]
# PLATFORM = "sensor"

STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
Custom integration: {NAME}
Version: {VERSION}
For issues: {ISSUE_URL}
-------------------------------------------------------------------
"""
