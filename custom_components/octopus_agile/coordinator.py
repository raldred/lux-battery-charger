"""DataUpdateCoordinator for octopus_agile."""
from __future__ import annotations

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.exceptions import ConfigEntryAuthFailed

from .api import (
    OctopusAgileApiClient,
    OctopusAgileApiClientAuthenticationError,
    OctopusAgileApiClientError,
)
from .const import DOMAIN, LOGGER


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class OctopusAgileDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        client: OctopusAgileApiClient,
        update_interval: int
    ) -> None:
        """Initialize."""
        self._client = client
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=update_interval),
        )

    def get_sensor_value(self, sensor_id):
        return None

    async def _async_update_data(self):
        """Update data via library."""
        try:
            import_data = await self._client.async_get_import_prices()
            export_data = await self._client.async_get_export_prices()

            combined_data = self._build_combined_array(import_data, export_data)

            return {
                "all": combined_data
            }
        except OctopusAgileApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except OctopusAgileApiClientError as exception:
            raise UpdateFailed(exception) from exception
        

    def _build_combined_array(self, import_data, export_data):
        """Build array of tariff data, combining import and export"""
        combined_data = list(
            map(
                lambda imp, exp: {
                    "from": imp["valid_from"],
                    "upto": imp["valid_to"],
                    "date": imp["valid_from"][:10],
                    "timefrom": imp["valid_from"][11:16],
                    "timeupto": imp["valid_to"][11:16],
                    "import": imp["value_inc_vat"],
                    "export": exp["value_inc_vat"]
                },
                import_data,
                export_data
            )
        )

        return combined_data
    
    def _import_low_data(self, data, sample=15):
        return sorted(
            data,
            key=lambda x: x["import"],
            reverse=False
        )[:sample]


    def _export_high_data(self, data, sample=15):
        return sorted(
            data,
            key=lambda x: x["export"],
            reverse=True
        )[:sample]

