"""Sample API Client."""
from __future__ import annotations

import asyncio
import socket

import aiohttp
import async_timeout

from .const import API_BASE

class OctopusAgileApiClientError(Exception):
    """Exception to indicate a general API error."""


class OctopusAgileApiClientCommunicationError(
    OctopusAgileApiClientError
):
    """Exception to indicate a communication error."""


class OctopusAgileApiClientAuthenticationError(
    OctopusAgileApiClientError
):
    """Exception to indicate an authentication error."""


class OctopusAgileApiClient:
    """Client to call Octopus API."""

    def __init__(
        self,
        import_tariff: str,
        export_tariff: str,
        region: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Client to call Octopus API."""
        self._import_tariff = import_tariff
        self._export_tariff = export_tariff
        self._region = region
        self._session = session

    async def async_get_import_prices(self) -> any:
        """Get import prices from the API."""
        return await self._api_wrapper(
            method="get", url=f"{API_BASE}{self._import_tariff}/electricity-tariffs/E-1R-{self._import_tariff}-{self._region}/standard-unit-rates/?page_size=96"
        )
    
    async def async_get_export_prices(self) -> any:
        """Get export prices from the API."""
        return await self._api_wrapper(
            method="get", url=f"{API_BASE}{self._export_tariff}/electricity-tariffs/E-1R-{self._export_tariff}-{self._region}/standard-unit-rates/?page_size=96"
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                if response.status in (401, 403):
                    raise OctopusAgileApiClientAuthenticationError(
                        "Invalid credentials",
                    )
                response.raise_for_status()
                result = await response.json()
                return result['results']

        except asyncio.TimeoutError as exception:
            raise OctopusAgileApiClientCommunicationError(
                "Timeout error fetching information",
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise OctopusAgileApiClientCommunicationError(
                "Error fetching information",
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            raise OctopusAgileApiClientError(
                "Something really wrong happened!"
            ) from exception
