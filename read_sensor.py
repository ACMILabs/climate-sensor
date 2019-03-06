import os, time
from datetime import datetime

import board
import busio
from adafruit_htu21d import HTU21D
import pytz
import requests

# Constants
LOCATION_NAME = os.getenv('LOCATION_NAME')
LOCATION_DESCRIPTION = os.getenv('LOCATION_DESCRIPTION')
XOS_CLIMATE_STATUS_ENDPOINT = os.getenv('XOS_CLIMATE_STATUS_ENDPOINT')
TIME_BETWEEN_READINGS = os.getenv('TIME_BETWEEN_READINGS')


def datetime_now():
    pytz_timezone = pytz.timezone('Australia/Melbourne')
    return datetime.now(pytz_timezone).isoformat()

i2c = busio.I2C(board.SCL, board.SDA)
sensor = HTU21D(i2c)

while True:
    # POST to XOS
    data = {
        'location': {
            'name': LOCATION_NAME,
            'description': LOCATION_DESCRIPTION
        },
        'temperature': sensor.temperature,
        'humidity': sensor.relative_humidity,
        'status_datetime': datetime_now()  # ISO8601 format
    }
    try:
        response = requests.post(XOS_CLIMATE_STATUS_ENDPOINT, json=data)
        response.raise_for_status()
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        print('Failed to connect to %s with error: %s' % (XOS_CLIMATE_STATUS_ENDPOINT, e))

    time.sleep(int(TIME_BETWEEN_READINGS))
