# Buienradar Precipitation Forecast sensor integration

import asyncio
import aiohttp
import voluptuous as vol
import logging

from datetime import datetime, timedelta

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import ( CONF_NAME, CONF_LATITUDE, CONF_LONGITUDE )
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.discovery import async_load_platform

_LOGGER = logging.getLogger(__name__)

DEFAULT_SCAN_INTERVAL = timedelta(minutes=5)

DEFAULT_NAME = 'Buienradar Precipitation Forecast'
DEFAULT_ICON = 'mdi:weather-pouring'

CONF_URL  = 'https://gpsgadget.buienradar.nl/data/raintext?lat=%s&lon=%s'
ATTR_DATA = 'forecast'

# ----------

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,

    vol.Inclusive(CONF_LATITUDE , "coordinates", "Latitude and longitude must exist together"): cv.latitude,
    vol.Inclusive(CONF_LONGITUDE, "coordinates", "Latitude and longitude must exist together"): cv.longitude,
})

@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    name = config.get(CONF_NAME)
    lat  = config.get(CONF_LATITUDE )
    lon  = config.get(CONF_LONGITUDE)
    url  = config.get(CONF_URL)

    if None in (lat, lon):
      lat = config.get(CONF_LATITUDE , hass.config.latitude)
      lon = config.get(CONF_LONGITUDE, hass.config.longitude)

    if None in (lat, lon):
        _LOGGER.error("Latitude or longitude not set in HomeAssistant config")
        return

    async_add_devices([RainForecastSensor(hass, name, lat, lon)], update_before_add=True)

async def async_get_rain_data(self): 
    async with self._session.get(CONF_URL % (self._lat, self._lon)) as response:
        responseText = await response.text()

    return responseText

# ----------

class RainForecastSensor(Entity):

    def __init__(self, hass, name, lat, lon):
        self._name    = name
        self._icon    = DEFAULT_ICON
        self._lat     = lat
        self._lon     = lon
        self._url     = url
        self._state   = None
        self._data    = []
        self._session = async_get_clientsession(hass)

    async def async_update(self):
        responseText = await async_get_rain_data(self)

        if not responseText:
            _LOGGER.error('API response error')
        else:
            total = 0.0
            data  = []

            lines = responseText.splitlines()

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

        # return self._state

    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        return self._icon

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
            ATTR_DATA      : self._data
        }

    @property
    def unit_of_measurement(self):
        return "mm"

