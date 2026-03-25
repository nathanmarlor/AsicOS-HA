"""DataUpdateCoordinator for AsicOS Bitcoin Miner."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_SYSTEM_INFO, DOMAIN, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class AsicOSCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator to fetch data from AsicOS miner."""

    def __init__(self, hass: HomeAssistant, host: str) -> None:
        """Initialize the coordinator."""
        self.host = host
        self.base_url = f"http://{host}"
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=SCAN_INTERVAL),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from the AsicOS API."""
        url = f"{self.base_url}{API_SYSTEM_INFO}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    if resp.status != 200:
                        raise UpdateFailed(
                            f"Error fetching data from {url}: HTTP {resp.status}"
                        )
                    data: dict[str, Any] = await resp.json()
                    return data
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with AsicOS at {self.host}: {err}") from err
        except TimeoutError as err:
            raise UpdateFailed(f"Timeout communicating with AsicOS at {self.host}") from err
