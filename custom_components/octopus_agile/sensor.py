"""Sensor platform for octopus_agile."""
from __future__ import annotations

import traceback

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    ATTR_CONFIGURATION_URL,
    ATTR_IDENTIFIERS,
    ATTR_MANUFACTURER,
    ATTR_MODEL,
    ATTR_NAME,
    ATTR_SW_VERSION,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import LOGGER, DOMAIN, VERSION, NAME, AUTHOR, ATTRIBUTION, ATTR_ENTRY_TYPE
from .coordinator import OctopusAgileDataUpdateCoordinator

SENSORS: dict[str, SensorEntityDescription] = {
    "import_prices": SensorEntityDescription(
        key="import_prices",
        translation_key="import_prices",
        suggested_display_precision=0,
        icon="mdi:format-list-numbered",
    ),
    "export_prices": SensorEntityDescription(
        key="export_prices",
        translation_key="export_prices",
        suggested_display_precision=0,
        icon="mdi:format-list-numbered",
    )
}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    """Set up the sensor platform."""
    coordinator: OctopusAgileDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []

    for sensor_types in SENSORS:
        sen = OctopusAgileSensor(coordinator, SENSORS[sensor_types], entry)
        entities.append(sen)

    async_add_entities(entities)


class OctopusAgileSensor(CoordinatorEntity, SensorEntity):
    """octopus_agile Sensor class."""

    _attr_attribution = ATTRIBUTION
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: OctopusAgileDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self.coordinator = coordinator
        self._attr_unique_id = f"{entity_description.key}"

        self._attributes = {}
        self._attr_extra_state_attributes = {}

        try:
            self._sensor_data = coordinator.get_sensor_value(entity_description.key)
        except Exception as ex:
            LOGGER.error(
                f"OctopusAgile - unable to get sensor value {ex} %s", traceback.format_exc()
            )
            self._sensor_data = None

        self._attr_device_info = {
            ATTR_IDENTIFIERS: {(DOMAIN, entry.entry_id)},
            ATTR_NAME: NAME, #entry.title,
            ATTR_MANUFACTURER: AUTHOR,
            ATTR_MODEL: NAME,
            ATTR_ENTRY_TYPE: DeviceEntryType.SERVICE,
            ATTR_SW_VERSION: VERSION,
            ATTR_CONFIGURATION_URL: "https://toolkit.solcast.com.au/",
        }

    @property
    def native_value(self):
        """Return the value reported by the sensor."""
        return self._sensor_data

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        try:
            self._sensor_data = self.coordinator.get_sensor_value(
                self.entity_description.key
            )
        except Exception as ex:
            LOGGER.error(
                f"OctopusAgile - unable to get sensor value {ex} %s", traceback.format_exc()
            )
            self._sensor_data = None
        self.async_write_ha_state()
