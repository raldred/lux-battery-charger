"""Adds config flow for Blueprint."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_create_clientsession
import homeassistant.helpers.config_validation as cv

from .api import (
    OctopusAgileApiClient,
    OctopusAgileApiClientAuthenticationError,
    OctopusAgileApiClientCommunicationError,
    OctopusAgileApiClientError,
)
from .const import DEFAULT_EXPORT_TARIFF, DEFAULT_IMPORT_TARIFF, DEFAULT_TARIFF_REGION, DEFAULT_UPDATE_INTERVAL, IMPORT_TARIFF, EXPORT_TARIFF, TARIFF_REGION, UPDATE_INTERVAL, NAME, DOMAIN, LOGGER


class OctopusAgileConfigFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Octopus Agile."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_tariff(
                    import_tariff=user_input[IMPORT_TARIFF],
                    export_tariff=user_input[EXPORT_TARIFF],
                    region=user_input[TARIFF_REGION]
                )
            except OctopusAgileApiClientAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except OctopusAgileApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except OctopusAgileApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=NAME,
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        IMPORT_TARIFF,
                        default=(user_input or {}).get(IMPORT_TARIFF, DEFAULT_IMPORT_TARIFF),
                    ): str,
                    vol.Required(
                        EXPORT_TARIFF,
                        default=(user_input or {}).get(EXPORT_TARIFF, DEFAULT_EXPORT_TARIFF),
                    ): str,
                    vol.Required(
                        TARIFF_REGION,
                        default=(user_input or {}).get(TARIFF_REGION, DEFAULT_TARIFF_REGION),
                    ): str,
                    vol.Required(
                        UPDATE_INTERVAL,
                        default=(user_input or {}).get(UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL),
                    ): cv.positive_int
                }
            ),
            errors=_errors,
        )

    async def _test_tariff(self, import_tariff: str, export_tariff: str, region: str) -> None:
        """Validate tariffs exist."""
        client = OctopusAgileApiClient(
            import_tariff=import_tariff,
            export_tariff=export_tariff,
            region=region,
            session=async_create_clientsession(self.hass)
        )
        await client.async_get_import_prices()
        await client.async_get_export_prices()
