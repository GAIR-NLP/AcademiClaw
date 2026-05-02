# F1 2023 Data Directory Overview

## 1. Resource Type Summary

| Resource Type | Description | Format | Purpose |
|---------------|-------------|--------|---------|
| Schedule Data | Complete 2023 season schedule information | CSV | Event planning and scheduling |
| Session Data | Practice, qualifying, race, sprint sessions, etc. | CSV | Lap time, telemetry, position analysis |
| Race Results | Final rankings and points for each race | CSV | Points calculation and ranking analysis |
| Driver Data | Driver basic information and statistics | CSV | Driver performance analysis |
| Team Data | Team basic information and statistics | CSV | Team performance analysis |
| Tire Data | Tire usage and performance data | CSV | Tire strategy analysis |
| Weather Data | Weather conditions during races | CSV | Weather impact on race analysis |
| Circuit Data | Circuit layout and characteristics data | CSV | Circuit impact on race analysis |
| API Documentation | FastF1 API usage documentation | Markdown | Development reference |
| Data Dictionary | Field definitions for all data | Markdown | Data analysis reference |
| Version Log | Data update and change records | Markdown | Data version management |

## 2. Data Source Entry Points

### 2.1 Main Data Sources
- **FastF1 Python Library**: Official API interface providing complete F1 event data
- **Formula 1 Official Website**: Supplementary data and official statistics
- **Ergast Developer API**: Historical data and supplementary information

### 2.2 API Endpoints
- `fastf1.get_session(2023, round_number, session_name)`: Get specified session data
- `fastf1.get_event_schedule(2023)`: Get complete schedule data
- `session.laps`: Get lap time data
- `session.get_telemetry()`: Get telemetry data
- `session.weather_data`: Get weather data
- `session.results`: Get race results

## 3. File Structure

```
f1_2023_data/
├── schedule.csv                     # Complete 2023 season schedule
├── drivers.csv                      # 2023 season driver information
├── teams.csv                        # 2023 season team information
├── circuits.csv                     # 2023 season circuit information
├── data_dictionary.md               # Data field definitions
├── api_documentation.md             # FastF1 API documentation
├── version_changelog.md             # Data version change log
├── Round_0_Pre-Season_Testing/      # Pre-season testing
│   ├── metadata.json                # Event metadata
│   ├── Practice_1/
│   │   ├── laps.csv                 # Lap time data
│   │   ├── car_data.csv             # Car telemetry data
│   │   ├── position_data.csv        # Position data
│   │   ├── drivers.csv              # Driver list
│   │   └── weather.csv              # Weather data
│   ├── Practice_2/
│   │   ├── laps.csv
│   │   ├── car_data.csv
│   │   ├── position_data.csv
│   │   ├── drivers.csv
│   │   └── weather.csv
│   └── Practice_3/
│       ├── laps.csv
│       ├── car_data.csv
│       ├── position_data.csv
│       ├── drivers.csv
│       └── weather.csv
├── Round_1_Bahrain_Grand_Prix/      # Bahrain Grand Prix
│   ├── metadata.json
│   ├── race_results.csv             # Race results
│   ├── Practice_1/
│   │   ├── laps.csv
│   │   ├── car_data.csv
│   │   ├── position_data.csv
│   │   ├── drivers.csv
│   │   └── weather.csv
│   ├── Practice_2/
│   │   ├── ...
│   ├── Practice_3/
│   │   ├── ...
│   ├── Qualifying/
│   │   ├── ...
│   └── Race/
│       ├── ...
├── Round_2_Saudi_Arabian_Grand_Prix/ # Saudi Arabian Grand Prix
│   ├── ... (same structure)
└── ... (remaining 20 races with identical structure)
```

## 4. Detailed Field Descriptions

### 4.1 schedule.csv
| Field Name | Data Type | Description |
|------------|-----------|-------------|
| RoundNumber | integer | Race round number |
| Country | string | Country |
| Location | string | Location |
| OfficialEventName | string | Official event name |
| EventDate | date | Event date |
| EventName | string | Event name |
| EventFormat | string | Event format |
| Session1 | string | Session 1 name |
| Session1Date | datetime | Session 1 date/time |
| Session1DateUtc | datetime | Session 1 UTC time |
| ... | ... | ... |

### 4.2 laps.csv
| Field Name | Data Type | Description |
|------------|-----------|-------------|
| Time | timedelta | Session time |
| Driver | string | Driver code |
| DriverNumber | integer | Car number |
| LapTime | timedelta | Lap time |
| LapNumber | float | Lap number |
| Stint | float | Consecutive driving stint |
| Sector1Time | timedelta | Sector 1 time |
| Sector2Time | timedelta | Sector 2 time |
| Sector3Time | timedelta | Sector 3 time |
| SpeedI1 | float | Speed trap 1 speed |
| SpeedI2 | float | Speed trap 2 speed |
| SpeedFL | float | Speed trap FL speed |
| SpeedST | float | Speed trap ST speed |
| Compound | string | Tire compound type |
| TyreLife | float | Tire age in laps |
| FreshTyre | boolean | Whether tire is new |
| Team | string | Team name |

### 4.3 car_data.csv
| Field Name | Data Type | Description |
|------------|-----------|-------------|
| Time | timedelta | Session time |
| Driver | string | Driver code |
| Speed | float | Speed (km/h) |
| Throttle | float | Throttle position (%) |
| Brake | boolean | Whether braking |
| DRS | boolean | Whether DRS is active |
| Gear | integer | Gear |
| RPM | integer | Engine RPM |
| nGear | float | Normalized gear |
| X | float | X coordinate |
| Y | float | Y coordinate |
| Z | float | Z coordinate |

### 4.4 weather.csv
| Field Name | Data Type | Description |
|------------|-----------|-------------|
| Time | timedelta | Session time |
| AirTemp | float | Air temperature (C) |
| Humidity | float | Humidity (%) |
| Pressure | float | Pressure (mbar) |
| Rainfall | boolean | Whether raining |
| TrackTemp | float | Track temperature (C) |
| WindDirection | integer | Wind direction (deg) |
| WindSpeed | float | Wind speed (km/h) |



```python

```

```python

```
