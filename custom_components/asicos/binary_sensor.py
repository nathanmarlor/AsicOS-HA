"""Binary sensor platform for AsicOS Bitcoin Miner."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import AsicOSConfigEntry
from .coordinator import AsicOSCoordinator
from .entity import AsicOSEntity


@dataclass(frozen=True, kw_only=True)
class AsicOSBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describe an AsicOS binary sensor."""

    value_fn: Callable[[dict[str, Any]], bool | None]


BINARY_SENSOR_DESCRIPTIONS: tuple[AsicOSBinarySensorEntityDescription, ...] = (
    AsicOSBinarySensorEntityDescription(
        key="mining_active",
        translation_key="mining_active",
        name="Mining Active",
        device_class=BinarySensorDeviceClass.RUNNING,
        value_fn=lambda d: d.get("pool", {}).get("state") == "mining",
    ),
    AsicOSBinarySensorEntityDescription(
        key="overheat",
        translation_key="overheat",
        name="Overheat",
        device_class=BinarySensorDeviceClass.HEAT,
        value_fn=lambda d: d.get("power", {}).get("overheat"),
    ),
    AsicOSBinarySensorEntityDescription(
        key="vr_fault",
        translation_key="vr_fault",
        name="VR Fault",
        device_class=BinarySensorDeviceClass.PROBLEM,
        value_fn=lambda d: d.get("power", {}).get("vr_fault"),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: AsicOSConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up AsicOS binary sensors."""
    coordinator = entry.runtime_data
    async_add_entities(
        AsicOSBinarySensor(coordinator, description)
        for description in BINARY_SENSOR_DESCRIPTIONS
    )


class AsicOSBinarySensor(AsicOSEntity, BinarySensorEntity):
    """Representation of an AsicOS binary sensor."""

    entity_description: AsicOSBinarySensorEntityDescription

    def __init__(
        self,
        coordinator: AsicOSCoordinator,
        description: AsicOSBinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.host}_{description.key}"

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        if self.coordinator.data is None:
            return None
        return self.entity_description.value_fn(self.coordinator.data)
