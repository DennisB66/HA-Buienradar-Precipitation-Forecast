from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_create_clientsession

import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from .const import ( DOMAIN )

class ForecastFlowHandler(data_entry_flow.FlowHandler):

    def __init__(self):
        self._errors = {}

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
          return self.async_create_entry( title = user_input[CONF_NAME], data = user_input)

        user_input = {}
        user_input[CONF_NAME] = self.hass.config.location_name
        user_input[CONF_LATITUDE] = self.hass.config.latitude
        user_input[CONF_LONGITUDE] = self.hass.config.longitude

        data_schema = {
            vol.Required( CONF_NAME,      default=user_input[CONF_NAME]     ): str,
            vol.Required( CONF_LATITUDE,  default=user_input[CONF_LATITUDE] ): cv.latitude,
            vol.Required( CONF_LONGITUDE, default=user_input[CONF_LONGITUDE]): cv.longitude,
        }

        return self.async_show_form( step_id="user", data_schema=vol.Schema(data_schema), errors=errors)
