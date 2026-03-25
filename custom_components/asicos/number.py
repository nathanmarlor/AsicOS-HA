"""Number platform for AsicOS Bitcoin Miner."""

from __future__ import annotations

import logging

import aiohttp

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import AsicOSConfigEntry
from .const import API_SYSTEM
from .coordinator import AsicOSCoordinator
from .entity import AsicOSEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: AsicOSConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up AsicOS number entities."""
    coordinator = entry.runtime_data
    async_add_entities([AsicOSFanOverride(coordinator)])


class AsicOSFanOverride(AsicOSEntity, NumberEntity):
    """Fan override control for AsicOS miner."""

    _attr_name = "Fan Override"
    _attr_icon = "mdi:fan"
    _attr_native_min_value = -1
    _attr_native_max_value = 100
    _attr_native_step = 5
    _attr_mode = NumberMode.SLIDER
    _attr_native_unit_of_measurement = "%"
    _attr_translation_key = "fan_override"

    def __init__(self, coordinator: AsicOSCoordinator) -> None:
        """Initialize the fan override number entity."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.host}_fan_override"

    @property
    def native_value(self) -> float | None:
        """Return the current fan override value."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get("power", {}).get("fan_override")

    async def async_set_native_value(self, value: float) -> None:
        """Set the fan override value."""
        url = f"{self.coordinator.base_url}{API_SYSTEM}"
        payload = {"fan_override": int(value)}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as resp:
                    if resp.status != 200:
                        _LOGGER.error(
                            "Failed to set fan override: HTTP %s", resp.status
                        )
                        return
        except (aiohttp.ClientError, TimeoutError) as err:
            _LOGGER.error("Error setting fan override: %s", err)
            return

        await self.coordinator.async_request_refresh()
