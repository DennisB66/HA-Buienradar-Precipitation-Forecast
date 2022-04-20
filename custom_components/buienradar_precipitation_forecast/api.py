from .const import API_URL

from datetime import datetime
import aiohttp
import logging

_LOGGER: logging.Logger = logging.getLogger(__package__)


class ForecastApiClient:
    def __init__(self, lat, lon, session: aiohttp.ClientSession) -> None:
        self._lat = lat
        self._lon = lon
        self._session = session

    async def async_get_data(self):
        async with self._session.get(API_URL % (self._lat, self._lon)) as response:
            response_text = await response.text()

        if not response_text:
            _LOGGER.error("API response error")

        total = 0.0
        _list = []

        # single rain entry = mm/h during 5 min
        lines = response_text.splitlines()

        total = round(total, 2)

        for line in lines:
            raw_data, time = line.split("|")

            time = datetime.today().strftime("%Y-%m-%d") + "T" + time + ":00"
            rain = round(10 ** ((int(raw_data) - 109) / 32) / 12, 2)
            total += rain

            entry = {"time": time, "rain": rain}
            _list.append(entry)

        total = round(total, 1)

        return {"total": total, "list": _list}
