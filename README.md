# Weather API Test Suite

This project contains automated tests for the WeatherStack API, specifically testing the current weather endpoint functionality.

## Overview

The test suite validates various aspects of the WeatherStack Current Weather API including:
- API key authentication
- Response structure validation
- Query parameter handling (city names, zip codes, coordinates, IP addresses)
- Language and unit parameter validation
- Error handling and status codes

## Project Structure

```
api_tests/
├── api_key.json                    # API key configuration
├── test_suites/
│   └── current_weather_api_test.py # Main test file
├── venv/                           # Python virtual environment
└── README.md                       # This file
```

## Prerequisites

- Python 3.10+
- WeatherStack API key (sign up at [weatherstack.com](https://weatherstack.com))

## Setup

1. **Clone/Download the project**
   ```bash
   cd api_tests
   ```

2. **Activate the virtual environment**
   ```bash
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies** (if not already installed)
   ```bash
   pip install pytest requests
   ```

4. **Configure API Key**
   
   Update the `api_key.json` file with your WeatherStack API key:
   ```json
   {
       "api_key": "your_actual_api_key_here"
   }
   ```

## Running Tests

### Run All Tests
```bash
pytest test_suites/current_weather_api_test.py -v
```

### Run Specific Test Classes
```bash
pytest test_suites/current_weather_api_test.py::TestCurrentWeatherAPI -v
```

### Run Individual Tests
```bash
pytest test_suites/current_weather_api_test.py::TestCurrentWeatherAPI::test_01_valid_access_key -v
```

### Run Tests with Detailed Output
```bash
pytest test_suites/current_weather_api_test.py -v -s
```

## Test Coverage

### 1. Authentication Tests
- **test_01_valid_access_key**: Validates successful API authentication
- **test_02_invalid_access_key**: Tests various invalid API key scenarios

### 2. Response Structure Validation
- **test_03_response_object_validation**: Ensures response contains required fields:
  - `request` object (type, query, language, unit)
  - `location` object (name, country, region, coordinates, timezone, etc.)
  - `current` object (weather data including temperature, conditions, wind, etc.)

### 3. Query Parameter Tests
- **test_04_query_parameter_validation**: Tests various query formats:
  - City names (e.g., "Taipei")
  - ZIP codes (e.g., "99501")
  - Coordinates (e.g., "40.7831,-73.9712")
  - IP addresses (e.g., "153.65.8.20")
  - Special queries (e.g., "fetch:ip")
  - Invalid queries and error handling

### 4. Language Parameter Tests
- **test_05_language_parameter_validation**: Tests supported languages:
  - Valid languages: Arabic (ar), Chinese (zh), Japanese (ja)
  - Invalid language codes and error responses

### 5. Unit Parameter Tests
- **test_06_unit_parameter_validation**: Tests temperature unit options:
  - Metric (m), Scientific (s), Fahrenheit (f)
  - Invalid unit codes and error handling

## API Endpoint

- **Base URL**: `http://api.weatherstack.com`
- **Current Weather Endpoint**: `/current`
- **Documentation**: [WeatherStack API Docs](https://weatherstack.com/documentation)

## Test Dependencies

The tests use pytest markers for:
- `@pytest.mark.failfast`: Stops execution on first failure
- `@pytest.mark.dependency()`: Manages test execution order
- `@pytest.mark.parametrize()`: Runs tests with multiple parameter sets

## Error Codes Tested

- **101**: Invalid API key
- **601**: Missing query parameter
- **605**: Invalid language parameter
- **606**: Invalid unit parameter
- **615**: Invalid query (location not found)

## Rate Limiting

The tests include 2-second delays between API calls to respect rate limiting policies.

## Notes

- Ensure your API key has sufficient quota for running all tests
- Some tests depend on others (dependency chain starts with valid API key test)
- The test suite automatically skips execution if `api_key.json` is not found
- All tests include detailed assertion messages for debugging

## Troubleshooting

1. **API Key Issues**: Ensure your API key is valid and has remaining quota
2. **Network Issues**: Check internet connectivity and API endpoint availability
3. **Test Failures**: Review assertion messages for specific failure details
4. **Rate Limiting**: If tests fail due to rate limits, increase sleep intervals

## Contributing

When adding new tests:
1. Follow the existing naming convention (`test_XX_descriptive_name`)
2. Include comprehensive docstrings with title, steps, and expected results
3. Add appropriate pytest markers and dependencies
4. Include rate limiting delays for API calls
5. Provide detailed assertion messages

## License

This is a testing project for educational/development purposes.