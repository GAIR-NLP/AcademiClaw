# F1 2023 Data Dictionary

## 1. Schedule Data (schedule.csv)

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
| Session2 | string | Session 2 name |
| Session2Date | datetime | Session 2 date/time |
| Session2DateUtc | datetime | Session 2 UTC time |
| Session3 | string | Session 3 name |
| Session3Date | datetime | Session 3 date/time |
| Session3DateUtc | datetime | Session 3 UTC time |
| Session4 | string | Session 4 name |
| Session4Date | datetime | Session 4 date/time |
| Session4DateUtc | datetime | Session 4 UTC time |
| Session5 | string | Session 5 name |
| Session5Date | datetime | Session 5 date/time |
| Session5DateUtc | datetime | Session 5 UTC time |

## 2. Lap Time Data (laps.csv)

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
| Sector1SessionTime | timedelta | Sector 1 session time |
| Sector2SessionTime | timedelta | Sector 2 session time |
| Sector3SessionTime | timedelta | Sector 3 session time |
| SpeedI1 | float | Speed trap 1 speed |
| SpeedI2 | float | Speed trap 2 speed |
| SpeedFL | float | Speed trap FL speed |
| SpeedST | float | Speed trap ST speed |
| Compound | string | Tire compound type |
| TyreLife | float | Tire age in laps |
| FreshTyre | boolean | Whether tire is new |
| Team | string | Team name |
| LapStartTime | timedelta | Lap start time |
| LapStartDate | datetime64[ns] | Lap start date/time |

## 3. Telemetry Data (car_data.csv)

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
| Distance | float | Distance (meters) |
| Status | string | Status |
| SessionTime | timedelta | Session time |
| LapNumber | integer | Lap number |
| Stint | integer | Consecutive driving stint |
| DriverAhead | string | Driver ahead code |
| GapToDriverAhead | timedelta | Gap to driver ahead |

## 4. Position Data (position_data.csv)

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| Time | timedelta | Session time |
| Driver | string | Driver code |
| X | float | X coordinate |
| Y | float | Y coordinate |
| Z | float | Z coordinate |
| Distance | float | Distance (meters) |
| Speed | float | Speed (km/h) |
| LapNumber | integer | Lap number |
| Stint | integer | Consecutive driving stint |

## 5. Driver Data (drivers.csv)

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| DriverNumber | integer | Car number |
| Driver | string | Driver code |
| Team | string | Team name |
| Country | string | Nationality |
| FullName | string | Full name |
| DOB | date | Date of birth |

## 6. Team Data (teams.csv)

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| Team | string | Team name |
| ConstructorId | string | Constructor ID |
| TeamPrincipal | string | Team principal |
| TechnicalDirector | string | Technical director |
| Chassis | string | Chassis model |
| Engine | string | Engine supplier |
| Country | string | Country |
| Budget | integer | Budget (USD) |

## 7. Circuit Data (circuits.csv)

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| CircuitId | string | Circuit ID |
| Name | string | Circuit name |
| Country | string | Country |
| City | string | City |
| Latitude | float | Latitude |
| Longitude | float | Longitude |
| Altitude | integer | Altitude (meters) |
| Length | float | Circuit length (km) |
| Turns | integer | Number of turns |
| DrsZones | integer | Number of DRS zones |
| FirstGrandPrix | integer | First Grand Prix year |
| LastGrandPrix | integer | Most recent Grand Prix year |

## 8. Weather Data (weather.csv)

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

## 9. Race Results (race_results.csv)

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| Position | integer | Finishing position |
| DriverNumber | integer | Car number |
| Driver | string | Driver code |
| Team | string | Team name |
| Laps | integer | Laps completed |
| Time | timedelta | Finishing time |
| GapToWinner | timedelta | Gap to winner |
| Reason | string | DNF reason (if applicable) |
| Points | float | Points earned |

## 10. Metadata (metadata.json)

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| race_name | string | Race name |
| round_number | integer | Race round number |
| event_format | string | Event format |
| location | string | Location |
| country | string | Country |
| date | string | Event date |
| sessions | array | Session list |
| drivers | array | Driver list |
| teams | array | Team list |
| circuit | object | Circuit information |
| created_at | string | Creation time |
| updated_at | string | Update time |
| version | string | Version number |
