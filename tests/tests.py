import requests

import read_sensor


def test_datetime_now():
    """
    Test that the datetime_now function includes a timezone.
    """

    datetime = read_sensor.datetime_now()
    assert '+' in datetime
