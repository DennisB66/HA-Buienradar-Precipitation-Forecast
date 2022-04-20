from homeassistant.components.sensor import SensorEntity
from homeassistant.const import ( CONF_NAME, CONF_LATITUDE, CONF_LONGITUDE )

from .const import DEFAULT_NAME, DEFAULT_ICON, DOMAIN, SENSOR
from .entity import ForecastEntity

import logging

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_devices):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices([ForecastSensor(coordinator, entry)])


class ForecastSensor(ForecastEntity, SensorEntity):

    def __init__(self, coordinator, entry):
        super().__init__(coordinator, entry)

        self._coordinator = coordinator
        self._entry = entry

        self._name = entry.data.get(CONF_NAME)
        self._lat  = entry.data.get(CONF_LATITUDE)
        self._lon  = entry.data.get(CONF_LONGITUDE)
        self._data = coordinator.data

        self._unique_id = entry.entry_id

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
        return self._data['total']

    @property
    def forecast(self):
        return self._data['list']

    @property
    def unit_of_measurement(self):
        return "mm"

    @property
    def extra_state_attributes(self):
        return {
            CONF_LATITUDE  : self._lat,
            CONF_LONGITUDE : self._lon,
            'forecast'     : self._data['list']
        }



