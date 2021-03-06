from homeassistant.const import CONF_NAME, CONF_LATITUDE, CONF_LONGITUDE
from homeassistant import config_entries
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN

import voluptuous as vol


class ForecastFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        self._errors = {}

    async def async_step_user(self, user_input=None):
        self._errors = {}

        # if self._async_current_entries():
        #     return self.async_abort(reason="single_instance_allowed")

        if user_input is None:
            user_input = {}
            user_input[CONF_NAME] = self.hass.config.location_name
            user_input[CONF_LATITUDE] = self.hass.config.latitude
            user_input[CONF_LONGITUDE] = self.hass.config.longitude

            return await self._show_config_form(user_input)

        if not await self._is_valid(user_input):
            return await self._show_config_form(user_input)

        return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

    async def _show_config_form(self, user_input):
        data_schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default=user_input[CONF_NAME]): str,
                vol.Required(
                    CONF_LATITUDE, default=user_input[CONF_LATITUDE]
                ): cv.latitude,
                vol.Required(
                    CONF_LONGITUDE, default=user_input[CONF_LONGITUDE]
                ): cv.longitude,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=self._errors
        )

    async def _is_valid(self, user_input=None):
        # todo: validate user input
        return True
