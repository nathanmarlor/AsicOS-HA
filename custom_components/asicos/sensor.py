"""Sensor platform for AsicOS Bitcoin Miner."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfPower,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import AsicOSConfigEntry
from .coordinator import AsicOSCoordinator
from .entity import AsicOSEntity


def _format_uptime(data: dict[str, Any]) -> str | None:
    """Format uptime_ms into 'Xd Xh Xm'."""
    ms = data.get("uptime_ms")
    if ms is None:
        return None
    total_seconds = int(ms / 1000)
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{days}d {hours}h {minutes}m"


def _compute_efficiency(data: dict[str, Any]) -> float | None:
    """Compute efficiency in J/TH (watts / (hashrate_ghs / 1000))."""
    watts = data.get("power", {}).get("watts")
    hashrate = data.get("hashrate_ghs")
    if watts is None or hashrate is None or hashrate == 0:
        return None
    ths = hashrate / 1000.0
    if ths == 0:
        return None
    return round(watts / ths, 1)


@dataclass(frozen=True, kw_only=True)
class AsicOSSensorEntityDescription(SensorEntityDescription):
    """Describe an AsicOS sensor."""

    value_fn: Callable[[dict[str, Any]], Any]


SENSOR_DESCRIPTIONS: tuple[AsicOSSensorEntityDescription, ...] = (
    AsicOSSensorEntityDescription(
        key="hashrate",
        translation_key="hashrate",
        name="Hashrate",
        icon="mdi:pickaxe",
        native_unit_of_measurement="GH/s",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda d: d.get("hashrate_ghs"),
    ),
    AsicOSSensorEntityDescription(
        key="efficiency",
        translation_key="efficiency",
        name="Efficiency",
        icon="mdi:lightning-bolt",
        native_unit_of_measurement="J/TH",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=_compute_efficiency,
    ),
    AsicOSSensorEntityDescription(
        key="power",
        translation_key="power",
        name="Power",
        icon="mdi:flash",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda d: d.get("power", {}).get("watts"),
    ),
    AsicOSSensorEntityDescription(
        key="temp_chip",
        translation_key="temp_chip",
        name="ASIC Temp",
        icon="mdi:thermometer",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda d: d.get("temps", {}).get("chip"),
    ),
    AsicOSSensorEntityDescription(
        key="temp_vr",
        translation_key="temp_vr",
        name="VRM Temp",
        icon="mdi:thermometer-alert",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda d: d.get("temps", {}).get("vr"),
    ),
    AsicOSSensorEntityDescription(
        key="temp_board",
        translation_key="temp_board",
        name="Board Temp",
        icon="mdi:thermometer-lines",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda d: d.get("temps", {}).get("board"),
    ),
    AsicOSSensorEntityDescription(
        key="input_voltage",
        translation_key="input_voltage",
        name="Input Voltage",
        icon="mdi:current-dc",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        value_fn=lambda d: d.get("power", {}).get("vin"),
    ),
    AsicOSSensorEntityDescription(
        key="input_current",
        translation_key="input_current",
        name="Input Current",
        icon="mdi:current-ac",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=2,
        value_fn=lambda d: d.get("power", {}).get("iin"),
    ),
    AsicOSSensorEntityDescription(
        key="vr_output_current",
        translation_key="vr_output_current",
        name="VR Output Current",
        icon="mdi:current-ac",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda d: d.get("power", {}).get("iout"),
    ),
    AsicOSSensorEntityDescription(
        key="fan1_speed",
        translation_key="fan1_speed",
        name="Fan 1 Speed",
        icon="mdi:fan",
        native_unit_of_measurement="rpm",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d.get("power", {}).get("fan0_rpm"),
    ),
    AsicOSSensorEntityDescription(
        key="fan2_speed",
        translation_key="fan2_speed",
        name="Fan 2 Speed",
        icon="mdi:fan",
        native_unit_of_measurement="rpm",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d.get("power", {}).get("fan1_rpm"),
    ),
    AsicOSSensorEntityDescription(
        key="fan1_duty",
        translation_key="fan1_duty",
        name="Fan 1 Duty",
        icon="mdi:fan",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d.get("power", {}).get("fan0_pct"),
    ),
    AsicOSSensorEntityDescription(
        key="fan2_duty",
        translation_key="fan2_duty",
        name="Fan 2 Duty",
        icon="mdi:fan",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d.get("power", {}).get("fan1_pct"),
    ),
    AsicOSSensorEntityDescription(
        key="accepted_shares",
        translation_key="accepted_shares",
        name="Accepted Shares",
        icon="mdi:check-circle",
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda d: d.get("pool", {}).get("accepted"),
    ),
    AsicOSSensorEntityDescription(
        key="rejected_shares",
        translation_key="rejected_shares",
        name="Rejected Shares",
        icon="mdi:close-circle",
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda d: d.get("pool", {}).get("rejected"),
    ),
    AsicOSSensorEntityDescription(
        key="share_rate",
        translation_key="share_rate",
        name="Share Rate",
        icon="mdi:chart-line",
        native_unit_of_measurement="/min",
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda d: d.get("pool", {}).get("share_rate"),
    ),
    AsicOSSensorEntityDescription(
        key="pool_difficulty",
        translation_key="pool_difficulty",
        name="Pool Difficulty",
        icon="mdi:target",
        value_fn=lambda d: d.get("pool", {}).get("difficulty"),
    ),
    AsicOSSensorEntityDescription(
        key="pool_rtt",
        translation_key="pool_rtt",
        name="Pool RTT",
        icon="mdi:timer",
        native_unit_of_measurement="ms",
        device_class=SensorDeviceClass.DURATION,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda d: d.get("pool", {}).get("rtt_ms"),
    ),
    AsicOSSensorEntityDescription(
        key="block_height",
        translation_key="block_height",
        name="Block Height",
        icon="mdi:cube-outline",
        value_fn=lambda d: d.get("pool", {}).get("block_height"),
    ),
    AsicOSSensorEntityDescription(
        key="best_diff_session",
        translation_key="best_diff_session",
        name="Best Diff Session",
        icon="mdi:trophy",
        value_fn=lambda d: round(d.get("mining", {}).get("session_best_diff", 0)),
    ),
    AsicOSSensorEntityDescription(
        key="best_diff_alltime",
        translation_key="best_diff_alltime",
        name="Best Diff All-Time",
        icon="mdi:trophy-award",
        value_fn=lambda d: round(d.get("mining", {}).get("alltime_best_diff", 0)),
    ),
    AsicOSSensorEntityDescription(
        key="hw_errors",
        translation_key="hw_errors",
        name="HW Errors",
        icon="mdi:alert-circle",
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda d: d.get("mining", {}).get("hw_errors"),
    ),
    AsicOSSensorEntityDescription(
        key="wifi_rssi",
        translation_key="wifi_rssi",
        name="WiFi RSSI",
        icon="mdi:wifi",
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=True,
        value_fn=lambda d: d.get("wifi_rssi"),
    ),
    AsicOSSensorEntityDescription(
        key="cpu_usage",
        translation_key="cpu_usage",
        name="CPU Usage",
        icon="mdi:cpu-64-bit",
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        value_fn=lambda d: d.get("cpu_usage"),
    ),
    AsicOSSensorEntityDescription(
        key="uptime",
        translation_key="uptime",
        name="Uptime",
        icon="mdi:clock-outline",
        value_fn=_format_uptime,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: AsicOSConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up AsicOS sensors."""
    coordinator = entry.runtime_data
    async_add_entities(
        AsicOSSensor(coordinator, description) for description in SENSOR_DESCRIPTIONS
    )


class AsicOSSensor(AsicOSEntity, SensorEntity):
    """Representation of an AsicOS sensor."""

    entity_description: AsicOSSensorEntityDescription

    def __init__(
        self,
        coordinator: AsicOSCoordinator,
        description: AsicOSSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.host}_{description.key}"

    @property
    def native_value(self) -> Any:
        """Return the sensor value."""
        if self.coordinator.data is None:
            return None
        return self.entity_description.value_fn(self.coordinator.data)
