"""The AsicOS Bitcoin Miner integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import CONF_HOST, DOMAIN, PLATFORMS
from .coordinator import AsicOSCoordinator

_LOGGER = logging.getLogger(__name__)

type AsicOSConfigEntry = ConfigEntry[AsicOSCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: AsicOSConfigEntry) -> bool:
    """Set up AsicOS Bitcoin Miner from a config entry."""
    host = entry.data[CONF_HOST]
    coordinator = AsicOSCoordinator(hass, host)

    await coordinator.async_config_entry_first_refresh()

    if coordinator.data is None:
        raise ConfigEntryNotReady(f"Unable to connect to AsicOS miner at {host}")

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: AsicOSConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
