from homeassistant.components.sensor import (
    STATE_CLASS_MEASUREMENT,
    ATTR_STATE_CLASS,
)

# Base component constants.
NAME = "Buienradar Precipitation Forecast"
DOMAIN = "buienradar"
VERSION = "2022.04.10"
ATTRIBUTION = "Buienradar precipitation forecast via http://..."

# Defaults
DEFAULT_NAME = NAME

# Platforms.
SENSOR = "sensor"
PLATFORMS = [SENSOR]

# Sensors
SENSORS = [
    {
        "name": "forecast",
        "icon": "mdi:rain",
        "unit_of_measurement": "mm",
        "key" : "forecast",
    }
]

