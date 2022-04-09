# Buienradar Precipitation Forecast sensor integration

import logging
from datetime import datetime
from datetime import timedelta
import random
import requests
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (CONF_RESOURCES)
from homeassistant.util import Throttle
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=5)

CONF_LAT = 'latitude'
CONF_LON = 'longitude'
CONF_URL = 'url'

ATTR_LAT  = 'latitude'
ATTR_LON  = 'longitude'
ATTR_DATA = 'forecast'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_LAT, default='51.0'): cv.string,
    vol.Required(CONF_LON, default='3.00'): cv.string,
    vol.Required(CONF_URL, default='https://gpsgadget.buienradar.nl/data/raintext?lat=%s&lon=%s'): cv.string,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    _LOGGER.debug('Setting up')
    lat = config.get(CONF_LAT)
    lon = config.get(CONF_LON)
    add_entities([RainForecastSensor(lat,lon)])

# ----------

class RainForecastSensor(Entity):

    def __init__(self, lat, lon):
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
            ATTR_LAT : self._lat,
            ATTR_LON : self._lon,
            ATTR_DATA: self._data
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

