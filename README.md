# AsicOS Bitcoin Miner - Home Assistant Integration

A custom Home Assistant integration for monitoring and controlling AsicOS-based Bitcoin miners.

## Features

- **24 sensors**: Hashrate, efficiency, power, temperatures, fan speeds, pool stats, mining stats, and more
- **3 binary sensors**: Mining active, overheat, VR fault
- **Fan override control**: Set fan speed from auto (-1) to 100%
- **Restart button**: Restart the miner from Home Assistant
- **5-second polling**: Near real-time updates
- **Diagnostics**: Full API dump for troubleshooting

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click the three dots menu in the top right, select **Custom repositories**
3. Add the repository URL and select **Integration** as the category
4. Search for "AsicOS Bitcoin Miner" and install
5. Restart Home Assistant

### Manual

1. Copy the `custom_components/asicos` folder into your Home Assistant `config/custom_components/` directory
2. Restart Home Assistant

## Configuration

1. Go to **Settings > Devices & Services > Add Integration**
2. Search for "AsicOS Bitcoin Miner"
3. Enter the IP address or hostname of your miner
4. The integration will validate the connection and create all entities

## Sensors

| Sensor | Unit | Description |
|--------|------|-------------|
| Hashrate | GH/s | Current mining hashrate |
| Efficiency | J/TH | Power efficiency (watts per terahash) |
| Power | W | Current power consumption |
| ASIC Temp | C | ASIC chip temperature |
| VRM Temp | C | Voltage regulator temperature |
| Board Temp | C | Board temperature |
| Input Voltage | V | Input voltage |
| Input Current | A | Input current |
| VR Output Current | A | Voltage regulator output current |
| Fan 1/2 Speed | rpm | Fan speeds |
| Fan 1/2 Duty | % | Fan duty cycles |
| Accepted Shares | - | Total accepted shares |
| Rejected Shares | - | Total rejected shares |
| Share Rate | /min | Current share rate |
| Pool Difficulty | - | Current pool difficulty |
| Pool RTT | ms | Round-trip time to pool |
| Block Height | - | Current block height |
| Best Diff Session | - | Best difficulty this session |
| Best Diff All-Time | - | Best difficulty all time |
| HW Errors | - | Hardware error count |
| WiFi RSSI | dBm | WiFi signal strength |
| CPU Usage | % | ESP32 CPU usage |
| Uptime | - | Formatted uptime (Xd Xh Xm) |

## Controls

- **Fan Override**: Number entity, -1 (auto) to 100% in steps of 5
- **Restart**: Button to restart the miner

## API

The integration communicates with the miner via its REST API:

- `GET /api/system/info` - Fetch all miner data
- `POST /api/system` - Update settings (e.g., fan override)
- `POST /api/system/restart` - Restart the miner
