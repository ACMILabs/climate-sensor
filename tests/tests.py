import requests

import read_sensor


def test_read_sensor():
    """
    Test the sensor readings return a value.
    """

    response = requests.get('http://localhost:1006')
    assert response.status_code == 200
    assert 'ambient_humidity 1.0' in response.text


def test_datetime_now():
    """
    Test that the datetime_now function returns a string with a timezone.
    """

    datetime = read_sensor.datetime_now()
    assert '+' in datetime
