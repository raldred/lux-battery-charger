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
        self.client = client
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=update_interval),
        )

    async def _async_update_data(self):
        """Update data via library."""
        try:
            await self.client.async_get_import_prices()
            return await self.client.async_get_export_prices()
        except OctopusAgileApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except OctopusAgileApiClientError as exception:
            raise UpdateFailed(exception) from exception
