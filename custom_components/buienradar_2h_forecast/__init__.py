import asyncio
import logging

from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, Config
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import ForecastApiClient
from .const import DOMAIN, PLATFORM, STARTUP_MESSAGE

from homeassistant.const import Platform
PLATFORMS: list[Platform] = [Platform.SENSOR]

_LOGGER: logging.Logger = logging.getLogger(__package__)



# async def async_setup(hass: HomeAssistant, config: Config):
#     """Set up this integration using YAML is not supported."""
#     return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    lat = entry.data.get(CONF_LATITUDE)
    lon = entry.data.get(CONF_LONGITUDE)

    session = async_get_clientsession(hass)
    client = ForecastApiClient(lat, lon, session)

    hass.data[DOMAIN][entry.entry_id] = client

#    hass.async_add_job(hass.config_entries.async_forward_entry_setup(entry, PLATFORM))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True