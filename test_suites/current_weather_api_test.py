import requests
import pytest
import json
import time

@pytest.fixture(scope="session")
def get_api_key():
    try:
        with open("api_key.json", "r") as f:
            api_key = json.load(f)
        return api_key["api_key"]
    except FileNotFoundError:
        pytest.skip("api_key.json not found, please create a file with the following content: {\"api_key\": \"your_api_key\"}")


class TestCurrentWeatherAPI:

    WEATHER_API_URL = "http://api.weatherstack.com"
    CURRENT_WEATHER_API_ENDPOINT = f"{WEATHER_API_URL}/current"

    @pytest.mark.failfast
    @pytest.mark.dependency()
    def test_01_valid_access_key(self, get_api_key):
        """
        Title: Test the api should return success when the access key is valid
        Steps:
            1. Send a request to the api with a valid access key and a valid query
        Expected:
            - The response should contain a success field and it should be True
            - The response should contain a location field and it should contain the name "Taipei"
        """
        status_code, response = self._get_current_weather_response("Taipei", get_api_key)
        assert status_code == 200 and 'error' not in response, "The response should contain a success field, actual response: " + str(response)
        assert response["location"]["name"] == "Taipei", "The response should contain a location field, actual response: " + str(response)
        self.SUCCESS_RESPONSE_TEMPLATE = response

    @pytest.mark.parametrize("key", ["", "1234567890", "!@#$%^&*("])
    @pytest.mark.dependency(depends=["test_01_valid_access_key"])
    def test_02_invalid_access_key(self, key):
        """
        Title: Test the api should return error when the access key is invalid
        Steps:
            1. Send a request to the api with an invalid access key and a valid query
        Expected:
            - The response should contain an error
            - The response should contain a success field and it should be False
        """
        _ , response = self._get_current_weather_response("Taipei", key)
        assert 'error' in response and response['error']['code'] == 101, "The response should contain an error, actual response: " + str(response)
        assert response["success"] == False, "The response should contain a success field, actual response: " + str(response)

    @pytest.mark.parametrize("object, keys", [
        ("request", ["type", "query", "language", "unit"]), 
        ("location", ["name", "country", "region", "lat", "lon", "timezone_id", "localtime", "localtime_epoch", "utc_offset"]), 
        ("current", ["observation_time", "temperature", "weather_code", "weather_icons", "weather_descriptions", "astro", "air_quality", "wind_speed", "wind_degree", "wind_dir", "pressure", "precip", "humidity", "cloudcover", "feelslike", "uv_index", "visibility"])
    ])
    @pytest.mark.dependency(depends=["test_01_valid_access_key"])
    def test_03_response_object_validation(self, object, keys, get_api_key):
        """
        Title: Test the api should return the correct response object when the access key is valid
        Steps:
            1. Send a request to the api with a valid access key and a valid query
            2. Validate the response object
        Expected:
            - The response object should contain the following keys: "request", "location", "current"
            - The response object "request" should contain the following keys: "type", "query", "language", "unit"
            - The response object "location" should contain the following keys: "name", "coun   try", "region", "lat", "lon", "timezone_id", "localtime", "localtime_epoch", "utc_offset"
            - The response object "current" should contain the following keys: "observation_time", "temperature", "weather_code", "weather_icons", "weather_descriptions", "wind_speed", "wind_degree", "wind_dir", "pressure", "precip", "humidity", "cloudcover", "feelslike", "uv_index", "visibility"
        """
        _ , response = self._get_current_weather_response("Taipei", get_api_key)
        response_obj = response[object]
        obj_keys = response_obj.keys()
        diff = set(obj_keys).difference(set(keys))
        assert not diff, "the response object " + object + " should contain the following keys: " + str(keys) + ", difference: " + str(diff)


    @pytest.mark.parametrize("query, valid, code", [
        ("Taipei", True, 200), # valid city name
        ("99501", True, 200), # valid zipcode
        ("40.7831,-73.9712", True, 200), # valid latlon
        ("153.65.8.20", True, 200), # valid ip
        ("fetch:ip", True, 200), # valid ip
        ("iepiat", False, 615), # invalid city name
        ("91, -180", False, 615), # invalid latlon
        ("255.255.255.255", False, 615), # invalid ip
        ("00000", False, 615), # invalid zipcode
        ("", False, 601), # empty query
        ]
    )
    @pytest.mark.dependency(depends=["test_01_valid_access_key"])
    def test_04_query_parameter_validation(self, query, valid, code, get_api_key):
        """
        Title: Test the api should return the correct response when the query is valid or invalid
        Steps:
            1. Send a request to the api with a valid query and a valid access key or an invalid query and a valid access key
            2. Validate the response
        Expected:
            - If the query is valid, the response should not contain an error
            - If the query is invalid, the response should contain an error and the error code should be 615 or 601
            - If the query is invalid, the response should contain a success field and it should be False
        """
        time.sleep(2)  # aviod rate limit
        status_code, response = self._get_current_weather_response(query, get_api_key)
        if valid:
            assert status_code == code and 'error' not in response, "The response should contain a success field, actual response: " + str(response)
        else:
            assert 'error' in response and response['error']['code'] == code, "The response should contain an error, actual response: " + str(response)
            assert response["success"] == False, "The response should contain a success field, actual response: " + str(response)

    @pytest.mark.parametrize("language, valid", [
        ("ar", True),
        ("zh", True),
        ("ja", True),
        ("xx", False),
    ])
    def test_05_language_parameter_validation(self, language, valid, get_api_key):
        """
        Title: Test the api should return the correct response when the language is valid or invalid
        Steps:
            1. Send a request to the api with a valid language and a valid access key or an invalid language and a valid access key
            2. Validate the response
        Expected:
            - If the language is valid, the response should not contain an error
            - If the language is invalid, the response should contain an error and the error code should be 605
            - If the language is invalid, the response should contain a success field and it should be False
        """
        time.sleep(2)  # aviod rate limit
        status_code, response = self._get_current_weather_response("Taipei", get_api_key, language=language)

        if valid:
            assert status_code == 200 and 'error' not in response, "The response should contain a success field, actual response: " + str(response)
        else:
            assert 'error' in response and response['error']['code'] == 605, "The response should contain an error, actual response: " + str(response)
            assert response["success"] == False, "The response should contain a success field, actual response: " + str(response)

    @pytest.mark.parametrize("units, valid", [
        ("m", True),  # Metric
        ("s", True),  # Scientific
        ("f", True),  # Fahrenheit
        ("k", False), # invalid
    ])
    def test_06_unit_parameter_validation(self, units, valid, get_api_key):
        """
        Title: Test the api should return the correct response when the unit is valid or invalid
        Steps:
            1. Send a request to the api with a valid unit and a valid access key or an invalid unit and a valid access key
            2. Validate the response
        Expected:
            - If the unit is valid, the response should not contain an error
            - If the unit is invalid, the response should contain an error and the error code should be 606
            - If the unit is invalid, the response should contain a success field and it should be False
        """
        time.sleep(2)  # aviod rate limit
        status_code, response = self._get_current_weather_response("Taipei", get_api_key, units=units)
        if valid:
            assert status_code == 200 and 'error' not in response, "The response should contain a success field, actual response: " + str(response)
        else:
            assert 'error' in response and response['error']['code'] == 606, "The response should contain an error, actual response: " + str(response)
            assert response["success"] == False, "The response should contain a success field, actual response: " + str(response)

    def _get_current_weather_response(self, query, get_api_key, **kwargs):
        url = f"{self.CURRENT_WEATHER_API_ENDPOINT}?access_key={get_api_key}&query={query}"
        if kwargs.get("language"):
            url += f"&language={kwargs.get('language')}"
        if kwargs.get("units"):
            url += f"&units={kwargs.get('units')}"
        response_raw = requests.get(url)
        response = response_raw.json()
        return response_raw.status_code, response