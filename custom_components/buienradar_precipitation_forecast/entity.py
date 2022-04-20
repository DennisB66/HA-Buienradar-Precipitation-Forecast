from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, NAME, VERSION, ATTRIBUTION


class ForecastEntity(CoordinatorEntity):
    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self.coordinator = coordinator
        self.entry = entry

    @property
    def unique_id(self):
        return self.entry.entry_id

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": NAME,
            "model": VERSION,
            "manufacturer": NAME,
        }

    @property
    def extra_state_attributes(self):
        return {
            "attribution": ATTRIBUTION,
            "id": str(self.coordinator.data.get("id")),
            "integration": DOMAIN,
        }
