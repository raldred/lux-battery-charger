"""Sensor platform for octopus_agile."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, NAME, AUTHOR
from .coordinator import OctopusAgileDataUpdateCoordinator

SENSORS: dict[str, SensorEntityDescription] = {
    "import_prices": SensorEntityDescription(
        key="import_prices",
        translation_key="import_prices",
        suggested_display_precision=0,
    ),
    "export_prices": SensorEntityDescription(
        key="export_prices",
        translation_key="export_prices",
        suggested_display_precision=0,
    )
}


async def async_setup_entry(hass, entry, async_add_entities: AddEntitiesCallback):
    """Set up the sensor platform."""
    coordinator: OctopusAgileDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []

    for sensor_types in SENSORS:
        sen = OctopusAgileSensor(coordinator, SENSORS[sensor_types], entry)
        entities.append(sen)

    async_add_entities(entities)


class OctopusAgileSensor(CoordinatorEntity, SensorEntity):
    """octopus_agile Sensor class."""

    def __init__(
        self,
        coordinator: OctopusAgileDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
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
            _LOGGER.error(
                f"OctopusAgile - unable to get sensor value {ex} %s", traceback.format_exc()
            )
            self._sensor_data = None

        self._attr_device_info = {
            ATTR_IDENTIFIERS: {(DOMAIN, entry.entry_id)},
            ATTR_NAME: NAME, #entry.title,
            ATTR_MANUFACTURER: AUTHOR,
            ATTR_MODEL: NAME,
            ATTR_ENTRY_TYPE: DeviceEntryType.SERVICE,
            ATTR_SW_VERSION: coordinator._version,
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
            _LOGGER.error(
                f"OctopusAgile - unable to get sensor value {ex} %s", traceback.format_exc()
            )
            self._sensor_data = None
        self.async_write_ha_state()
