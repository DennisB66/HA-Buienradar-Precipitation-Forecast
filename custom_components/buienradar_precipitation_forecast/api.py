""" buienradar precipiation forecast: API client """

from datetime import datetime

import logging
import aiohttp

from .const import API_URL

_LOGGER: logging.Logger = logging.getLogger(__package__)

HISTDATA_LEN = 4
FORECAST_LEN = 4


class ForecastApiClient:
    """ class to implement API client """

    def __init__(self, lat, lon, session: aiohttp.ClientSession) -> None:
        """ initialize class """
        self._lat = lat
        self._lon = lon
        # self._forecast_size = forecast_size
        # self._histdata_size = histdata_size
        self._session = session
        self._total = 0.0
        self._list = []

    def _today(self, time):
        """ convert time as "hh:mm" to the datetime format (yyyy-mm-ddThh:mm:ss) """
        return datetime.today().strftime("%Y-%m-%d") + "T" + time + ":00"

    def _clr_histdata(self, lines):
        """ reset list / remove (old) forecast / retain (new) history """

        # skip when list is empty (only at first call)
        if len(self._list) == 0:
            return

        # forecast data starting at <time>
        time = self._today(lines[0].split("|")[1])

        for i in range(len(self._list)):
            # remove forecast data starting at new <time>
            if self._list[i]["time"] == time:
                count = min(len(self._list) - i, FORECAST_LEN)
                break
        else:
            # remove forecast data starting at old <time>
            count = FORECAST_LEN

        # remove previous forecast (tail)
        del self._list[-count:]
        # remove obsolete histdata (head)
        del self._list[0 : max(0, len(self._list) - HISTDATA_LEN)]

    def _add_forecast(self, lines):
        """ """
        self._total = 0.0

        for i in range(FORECAST_LEN):
            rain, time = lines[i].split("|")
            time = self._today(time)
            rain = round(10 ** ((int(rain) - 109) / 32) / 12, 2)
            self._total += rain

            item = {"time": time, "rain": rain}
            self._list.append(item)

        self._total = round(self._total, 1)

    async def async_get_data(self):
        """ fetch data from API (single rain entry = mm/h during 5 min) """

        async with self._session.get(API_URL % (self._lat, self._lon)) as response:
            response_text = await response.text()

        if not response_text:
            _LOGGER.error("API response error")

        lines = response_text.splitlines()

        self._clr_histdata(lines)
        self._add_forecast(lines)

        return {"total": self._total, "list": self._list}
