"""Diagnostics support for AsicOS Bitcoin Miner."""

from __future__ import annotations

from typing import Any

from homeassistant.core import HomeAssistant

from . import AsicOSConfigEntry


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: AsicOSConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data
    return {
        "config": {
            "host": entry.data.get("host"),
        },
        "api_response": coordinator.data,
    }
