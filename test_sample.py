from WeatherDB import cur,getRequestToWheaterApi,loadWeatherDatatoSqlite3


def test_getRequestToWheaterApi_check_country_equals_Israel():
    res = getRequestToWheaterApi('Tel Aviv','f')
    api_response = loadWeatherDatatoSqlite3(res)
    location = api_response["location"]
    assert location["country"] == 'Israel'

def test_getRequestToWheaterApi_check_country_equals_united_states():
    res = getRequestToWheaterApi('New York','f')
    api_response = loadWeatherDatatoSqlite3(res)
    location = api_response["location"]
    assert location["country"] == 'United States of America'   
