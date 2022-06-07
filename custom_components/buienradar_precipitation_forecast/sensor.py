from datetime import timedelta
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_NAME, CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.util import Throttle

from .const import DEFAULT_NAME, DEFAULT_ICON, DOMAIN

_LOGGER: logging.Logger = logging.getLogger(__package__)

SCAN_INTERVAL = timedelta(seconds=300)


async def async_setup_entry(hass, entry, async_add_devices):
    client = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([ForecastSensor(entry, client)], True)


class ForecastSensor(SensorEntity):
    def __init__(self, entry, client):

        self._entry = entry
        self._api = client

        self._unique_id = entry.entry_id

        self._name = entry.data.get(CONF_NAME)
        self._lat = entry.data.get(CONF_LATITUDE)
        self._lon = entry.data.get(CONF_LONGITUDE)
        self._data = []

    @Throttle(SCAN_INTERVAL)
    async def async_update(self):
        self._data = await self._api.async_get_data()
        _LOGGER.debug(self._data["total"])

    @property
    def name(self):
        return f"{DEFAULT_NAME} {self._name}"

    @property
    def icon(self):
        return DEFAULT_ICON

    @property
    def latitude(self):
        return self._lat

    @property
    def longitude(self):
        return self._lon

    @property
    def state(self):
        return self._data["total"]

    @property
    def forecast(self):
        return self._data["list"]

    @property
    def unit_of_measurement(self):
        return "mm"

    @property
    def extra_state_attributes(self):
        return {
            CONF_LATITUDE: self._lat,
            CONF_LONGITUDE: self._lon,
            "forecast": self._data["list"],
        }
