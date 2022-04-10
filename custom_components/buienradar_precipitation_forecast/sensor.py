# Buienradar Precipitation Forecast sensor integration

import voluptuous as vol
import requests
import logging

from datetime import datetime, timedelta

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_NAME,
    CONF_LATITUDE,
    CONF_LONGITUDE,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType
from homeassistant.util import Throttle
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=5)

DEFAULT_NAME = "Buienradar Precipitation Forecast"

CONF_URL  = 'url'
ATTR_DATA = 'forecast'

# ----------

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,

    vol.Inclusive(CONF_LATITUDE , "coordinates", "Latitude and longitude must exist together"): cv.latitude,
    vol.Inclusive(CONF_LONGITUDE, "coordinates", "Latitude and longitude must exist together"): cv.longitude,

    vol.Optional(CONF_URL, default='https://gpsgadget.buienradar.nl/data/raintext?lat=%s&lon=%s'): cv.string,
})

def setup_platform(hass: HomeAssistant, config: ConfigType, add_entities, discovery_info=None):
    _LOGGER.debug('Setting up')
    fname = config.get(CONF_NAME)
    lat   = config.get(CONF_LATITUDE )
    lon   = config.get(CONF_LONGITUDE)

    if None in (lat, lon):
      lat = config.get(CONF_LATITUDE , hass.config.latitude)
      lon = config.get(CONF_LONGITUDE, hass.config.longitude)

    if None in (lat, lon):
        _LOGGER.error("Latitude or longitude not set in HomeAssistant config")
        return

    add_entities([RainForecastSensor(fname, lat,lon)])

# ----------

class RainForecastSensor(Entity):

    def __init__(self, fname, lat, lon):
        self._name = fname
        self._lat = lat
        self._lon = lon
        self._url = "https://gpsgadget.buienradar.nl/data/raintext?lat=%s&lon=%s"
        self._state = None
        self._data = []

    @property
    def name(self):
        return 'Buienradar Precipitation Forecast'

    @property
    def state(self):
        return self._state

    @property
    def latitude(self):
        return self._lat

    @property
    def longitude(self):
        return self._lon

    @property
    def data(self):
        return self._data

    @property
    def extra_state_attributes(self):
        return {
            CONF_NAME      : self._name,
            CONF_LATITUDE  : self._lat,
            CONF_LONGITUDE : self._lon,
            CONF_URL       : self._url,
            ATTR_DATA      : self._data
        }

    @property
    def unit_of_measurement(self):
        return "mm"

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        _LOGGER.debug('Updating')

        try:
            url = self._url % (self._lat, self._lon)
            response = requests.get(self._url % (self._lat, self._lon))

            if not response:
                _LOGGER.error('API response error')
            else:
                total = 0.0
                data  = []

                lines = response.text.splitlines()

                total = round( total, 2)

                for line in lines:
                    raw_data, time = line.split("|")
                    time = datetime.today().strftime('%Y-%m-%d') + "T" + time + ":00"
                    # single rain entry = mm/h during 5 min
                    rain = round( 10 ** ((int( raw_data) - 109) / 32) / 12, 2)
                    total += rain
                    entry = {"time": time, "rain": rain}
                    data.append( entry)

                self._state = round( total, 1)
                self._data = data

        except requests.exceptions.RequestException as exc:
            _LOGGER.error('Error %r', exc)
            self._data = []
            return False
