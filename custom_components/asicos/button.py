"""Button platform for AsicOS Bitcoin Miner."""

from __future__ import annotations

import logging

import aiohttp

from homeassistant.components.button import ButtonDeviceClass, ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import AsicOSConfigEntry
from .const import API_SYSTEM_RESTART
from .coordinator import AsicOSCoordinator
from .entity import AsicOSEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: AsicOSConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up AsicOS button entities."""
    coordinator = entry.runtime_data
    async_add_entities([AsicOSRestartButton(coordinator)])


class AsicOSRestartButton(AsicOSEntity, ButtonEntity):
    """Restart button for AsicOS miner."""

    _attr_name = "Restart"
    _attr_icon = "mdi:restart"
    _attr_device_class = ButtonDeviceClass.RESTART
    _attr_translation_key = "restart"

    def __init__(self, coordinator: AsicOSCoordinator) -> None:
        """Initialize the restart button."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.host}_restart"

    async def async_press(self) -> None:
        """Handle the button press."""
        url = f"{self.coordinator.base_url}{API_SYSTEM_RESTART}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url, timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status != 200:
                        _LOGGER.error(
                            "Failed to restart miner: HTTP %s", resp.status
                        )
        except (aiohttp.ClientError, TimeoutError) as err:
            _LOGGER.error("Error restarting miner: %s", err)
