"""Constants for the AsicOS Bitcoin Miner integration."""

from typing import Final

DOMAIN: Final = "asicos"
CONF_HOST: Final = "host"
SCAN_INTERVAL: Final = 5

# API endpoints
API_SYSTEM_INFO: Final = "/api/system/info"
API_SYSTEM: Final = "/api/system"
API_SYSTEM_RESTART: Final = "/api/system/restart"

# Sensor keys - top level
KEY_HASHRATE: Final = "hashrate_ghs"
KEY_CHIP_COUNT: Final = "chip_count"
KEY_UPTIME_MS: Final = "uptime_ms"
KEY_FREE_HEAP: Final = "free_heap"
KEY_WIFI_RSSI: Final = "wifi_rssi"
KEY_CPU_USAGE: Final = "cpu_usage"

# Sensor keys - temps
KEY_TEMP_CHIP: Final = "chip"
KEY_TEMP_VR: Final = "vr"
KEY_TEMP_BOARD: Final = "board"

# Sensor keys - power
KEY_POWER_VIN: Final = "vin"
KEY_POWER_IIN: Final = "iin"
KEY_POWER_VOUT: Final = "vout"
KEY_POWER_IOUT: Final = "iout"
KEY_POWER_WATTS: Final = "watts"
KEY_POWER_INPUT_WATTS: Final = "input_watts"
KEY_POWER_FAN0_RPM: Final = "fan0_rpm"
KEY_POWER_FAN1_RPM: Final = "fan1_rpm"
KEY_POWER_FAN0_PCT: Final = "fan0_pct"
KEY_POWER_FAN1_PCT: Final = "fan1_pct"
KEY_POWER_FAN_OVERRIDE: Final = "fan_override"
KEY_POWER_FAN_MODE: Final = "fan_mode"
KEY_POWER_OVERHEAT: Final = "overheat"
KEY_POWER_VR_FAULT: Final = "vr_fault"

# Sensor keys - mining
KEY_MINING_SESSION_BEST: Final = "session_best_diff"
KEY_MINING_ALLTIME_BEST: Final = "alltime_best_diff"
KEY_MINING_TOTAL_SHARES: Final = "total_shares_submitted"
KEY_MINING_HW_ERRORS: Final = "hw_errors"

# Sensor keys - pool
KEY_POOL_STATE: Final = "state"
KEY_POOL_ACCEPTED: Final = "accepted"
KEY_POOL_REJECTED: Final = "rejected"
KEY_POOL_DIFFICULTY: Final = "difficulty"
KEY_POOL_RTT: Final = "rtt_ms"
KEY_POOL_BLOCK_HEIGHT: Final = "block_height"
KEY_POOL_SHARE_RATE: Final = "share_rate"

# Device info keys
KEY_BOARD_NAME: Final = "board_name"
KEY_ASIC_MODEL: Final = "asic_model"
KEY_FIRMWARE_VERSION: Final = "firmware_version"

# Platforms
PLATFORMS: Final = ["sensor", "binary_sensor", "number", "button"]
