# Weather API Test Suite

This project contains comprehensive automated tests for the WeatherStack API, specifically testing the current weather endpoint functionality with various scenarios and edge cases.

## Overview

The test suite validates critical aspects of the WeatherStack Current Weather API including:
- API key authentication and authorization
- Response structure and data validation
- Query parameter handling (city names, ZIP codes, coordinates, IP addresses)
- Language and unit parameter validation
- Error handling and HTTP status codes
- Rate limiting compliance

## Project Structure

```
weather_api_test/
├── README.md                       # Project documentation
├── requirements.txt               # Python dependencies
├── test_suites/
│   └── current_weather_api_test.py # Comprehensive test suite
└── api_key.json                   # API key configuration (to be created)
```

## Prerequisites

- **Python**: 3.10 or higher
- **WeatherStack API Key**: Sign up at [weatherstack.com](https://weatherstack.com) for a free API key
- **Internet Connection**: Required for API calls during testing

## Setup Instructions

### 1. Environment Setup
```bash
cd weather_api_test
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

Alternatively, install manually:
```bash
pip install pytest requests
```

### 3. Configure API Key

Create an `api_key.json` file in the project root:
```json
{
    "api_key": "your_actual_weatherstack_api_key_here"
}
```

> **Note**: Keep your API key secure and do not commit it to version control.

## Running Tests

### Run All Tests
```bash
pytest test_suites/current_weather_api_test.py -v
```

### Run Specific Test Class
```bash
pytest test_suites/current_weather_api_test.py::TestCurrentWeatherAPI -v
```

### Run Individual Tests
```bash
pytest test_suites/current_weather_api_test.py::TestCurrentWeatherAPI::test_01_valid_access_key -v
```

### Run with Detailed Output
```bash
pytest test_suites/current_weather_api_test.py -v -s
```

### Run with Fail-Fast (Stop on First Failure)
```bash
pytest test_suites/current_weather_api_test.py -x -v
```

## Test Coverage

| Test Category | Test Method | Description | Scenarios Tested |
|---------------|-------------|-------------|------------------|
| **Authentication** | `test_01_valid_access_key` | Validates successful API authentication with valid key | ✅ Valid API key with Taipei query |
| **Authentication** | `test_02_invalid_access_key` | Tests various invalid API key scenarios | ❌ Empty key, numeric key, special characters |
| **Response Structure** | `test_03_response_object_validation` | Ensures response contains all required fields and objects | ✅ `request`, `location`, `current` objects with all expected keys |
| **Query Parameters** | `test_04_query_parameter_validation` | Tests various query formats and validation | ✅ City names, ZIP codes, coordinates, IP addresses<br/>❌ Invalid locations, malformed queries, empty queries |
| **Localization** | `test_05_language_parameter_validation` | Tests language parameter support | ✅ Arabic (ar), Chinese (zh), Japanese (ja)<br/>❌ Invalid language codes |
| **Units** | `test_06_unit_parameter_validation` | Tests temperature unit options | ✅ Metric (m), Scientific (s), Fahrenheit (f)<br/>❌ Invalid unit codes |

### Test Details

#### Authentication Tests (2 tests)
- **Valid Key**: Confirms successful authentication and data retrieval
- **Invalid Keys**: Tests empty, numeric, and special character keys (Error Code: 101)

#### Response Structure Validation (1 test with multiple scenarios)
Validates all response objects contain required fields:
- **`request`**: type, query, language, unit
- **`location`**: name, country, region, lat, lon, timezone_id, localtime, localtime_epoch, utc_offset
- **`current`**: observation_time, temperature, weather_code, weather_icons, weather_descriptions, astro, air_quality, wind_speed, wind_degree, wind_dir, pressure, precip, humidity, cloudcover, feelslike, uv_index, visibility

#### Query Parameter Tests (10 scenarios)
| Query Type | Examples | Expected Result |
|------------|----------|----------------|
| City Names | "Taipei" | ✅ Success |
| ZIP Codes | "99501" | ✅ Success |
| Coordinates | "40.7831,-73.9712" | ✅ Success |
| IP Addresses | "153.65.8.20", "fetch:ip" | ✅ Success |
| Invalid Queries | "iepiat", "91, -180", "255.255.255.255", "00000" | ❌ Error 615 |
| Empty Query | "" | ❌ Error 601 |

## API Configuration

- **Base URL**: `http://api.weatherstack.com`
- **Endpoint**: `/current`
- **Method**: GET
- **Documentation**: [WeatherStack API Documentation](https://weatherstack.com/documentation)

## Error Codes Handled

| Code | Description | Test Coverage |
|------|-------------|---------------|
| 101 | Invalid API Access Key | ✅ Tested |
| 601 | Missing Query Parameter | ✅ Tested |
| 605 | Invalid Language Parameter | ✅ Tested |
| 606 | Invalid Unit Parameter | ✅ Tested |
| 615 | Invalid Query (Location Not Found) | ✅ Tested |

## Test Framework Features

- **Pytest Markers**:
  - `@pytest.mark.failfast`: Stops execution on first failure
  - `@pytest.mark.dependency()`: Manages test execution order and dependencies
  - `@pytest.mark.parametrize()`: Runs tests with multiple parameter sets
- **Rate Limiting**: 2-second delays between API calls to respect rate limits
- **Error Handling**: Comprehensive error message validation and assertion details
- **Dependency Management**: Tests depend on valid API key verification

## Best Practices

- **API Key Security**: Store API keys in `api_key.json` and exclude from version control
- **Rate Limiting**: Built-in delays prevent API quota exhaustion
- **Test Dependencies**: Failed authentication tests will skip dependent tests
- **Detailed Assertions**: All failures include full response details for debugging

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **API Key Not Found** | Create `api_key.json` with valid WeatherStack API key |
| **Rate Limit Exceeded** | Wait for quota reset or upgrade API plan |
| **Network Connectivity** | Check internet connection and API endpoint availability |
| **Test Failures** | Review assertion messages and verify API key quota |
| **Import Errors** | Install required dependencies: `pip install pytest requests` |

## Contributing

When adding new tests:
1. Follow the existing naming convention (`test_XX_descriptive_name`)
2. Add appropriate pytest markers and dependencies
3. Include comprehensive docstrings with title, steps, and expected results
4. Update this README with new test coverage information

## License

This project is provided as-is for testing and educational purposes.
