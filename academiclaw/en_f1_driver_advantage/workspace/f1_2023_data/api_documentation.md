# F1 2023 Dataset API Documentation

## 1. Overview

This document provides API interface documentation for the F1 2023 dataset, helping developers quickly understand how to retrieve and use F1 event data.

## 2. Basic Information

- **API Version**: v1
- **Base URL**: `https://api.f1.com/v1/`
- **Authentication**: API key authentication
- **Response Format**: JSON

## 3. Authentication

All API requests require a valid API key in the request header:

```
Authorization: Bearer YOUR_API_KEY
```

## 4. Rate Limits

- **Free Account**: 100 requests/hour
- **Standard Account**: 1000 requests/hour
- **Premium Account**: 10000 requests/hour

## 5. Core API Endpoints

### 5.1 Get Schedule Data

**Endpoint**: `/2023/schedule`

**Method**: GET

**Parameters**:
- `round`: Optional, specify round number

**Example Request**:
```
GET https://api.f1.com/v1/2023/schedule
Authorization: Bearer YOUR_API_KEY
```

**Example Response**:
```json
{
  "rounds": [
    {
      "round_number": 1,
      "country": "Bahrain",
      "location": "Sakhir",
      "event_name": "Bahrain Grand Prix",
      "event_date": "2023-03-05",
      "sessions": [
        {
          "name": "Practice 1",
          "date": "2023-03-03T16:30:00Z",
          "type": "practice"
        },
        // Other sessions...
      ]
    },
    // Other rounds...
  ]
}
```

### 5.2 Get Driver Data

**Endpoint**: `/2023/drivers`

**Method**: GET

**Parameters**:
- `team`: Optional, filter by team
- `driver_number`: Optional, filter by car number

**Example Request**:
```
GET https://api.f1.com/v1/2023/drivers
Authorization: Bearer YOUR_API_KEY
```

### 5.3 Get Team Data

**Endpoint**: `/2023/teams`

**Method**: GET

**Example Request**:
```
GET https://api.f1.com/v1/2023/teams
Authorization: Bearer YOUR_API_KEY
```

### 5.4 Get Lap Time Data

**Endpoint**: `/2023/{round}/{session}/laps`

**Method**: GET

**Parameters**:
- `round`: Round number
- `session`: Session type (practice1, practice2, practice3, qualifying, sprint, race)
- `driver`: Optional, filter by driver code

**Example Request**:
```
GET https://api.f1.com/v1/2023/1/practice1/laps?driver=VER
Authorization: Bearer YOUR_API_KEY
```

### 5.5 Get Race Results

**Endpoint**: `/2023/{round}/race/results`

**Method**: GET

**Parameters**:
- `round`: Round number

**Example Request**:
```
GET https://api.f1.com/v1/2023/1/race/results
Authorization: Bearer YOUR_API_KEY
```

## 6. Data Download API

### 6.1 Download Single File

**Endpoint**: `/2023/download/{file_path}`

**Method**: GET

**Parameters**:
- `file_path`: File path

**Example Request**:
```
GET https://api.f1.com/v1/2023/download/Round_1_Bahrain_Grand_Prix/Practice_1/laps.csv
Authorization: Bearer YOUR_API_KEY
```

### 6.2 Batch Download Files

**Endpoint**: `/2023/download/batch`

**Method**: POST

**Parameters**:
- `files`: Array of file paths

**Example Request**:
```json
POST https://api.f1.com/v1/2023/download/batch
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "files": [
    "Round_1_Bahrain_Grand_Prix/Practice_1/laps.csv",
    "Round_1_Bahrain_Grand_Prix/Practice_2/laps.csv"
  ]
}
```

## 7. Error Handling

| Status Code | Description |
|-------------|-------------|
| 200 | Request successful |
| 400 | Bad request parameters |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Resource not found |
| 429 | Too many requests |
| 500 | Internal server error |

## 8. WebSocket API

### 8.1 Real-time Data Subscription

**Endpoint**: `wss://api.f1.com/v1/2023/live`

**Authentication**: API key required at connection time

**Subscription Example**:
```json
{
  "type": "subscribe",
  "events": [
    "lap_data",
    "position_data",
    "weather_data"
  ],
  "session": "round_1_race"
}
```

## 9. SDKs and Client Libraries

- **Python**: `pip install f1-data-sdk`
- **JavaScript**: `npm install f1-data-sdk`
- **Java**: Available on Maven Central
- **C#**: Available on NuGet

## 10. Data Update Frequency

- **Schedule Data**: Real-time updates
- **Driver and Team Data**: Daily updates
- **Session Data**: Updated within 15 minutes after session ends
- **Real-time Data**: 3-second delay

## 11. Data Copyright and Terms of Use

All data is protected by F1 official copyright and is only permitted for non-commercial purposes. Commercial use requires a separate license application.

## 12. Support

- **Documentation**: https://docs.f1.com/
- **API Status**: https://status.f1.com/
- **Support Email**: api-support@f1.com
- **Community Forum**: https://forum.f1.com/
