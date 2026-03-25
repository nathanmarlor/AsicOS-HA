"""Base entity for AsicOS Bitcoin Miner."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, KEY_ASIC_MODEL, KEY_BOARD_NAME, KEY_FIRMWARE_VERSION
from .coordinator import AsicOSCoordinator


class AsicOSEntity(CoordinatorEntity[AsicOSCoordinator]):
    """Base entity for AsicOS."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: AsicOSCoordinator) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.host)},
            name=coordinator.data.get(KEY_BOARD_NAME, "AsicOS Miner"),
            manufacturer="AsicOS",
            model=coordinator.data.get(KEY_ASIC_MODEL, "Unknown"),
            sw_version=coordinator.data.get(KEY_FIRMWARE_VERSION, "Unknown"),
            configuration_url=f"http://{coordinator.host}",
        )
