import os
import time
from datetime import datetime

import board
import pytz
import requests

import busio
from adafruit_htu21d import HTU21D
from prometheus_client import Gauge, start_http_server


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
temperature_gauge = Gauge('ambient_temperature', 'Ambient temperature')
humidity_gauge = Gauge('ambient_humidity', 'Ambient humidity')

if __name__ == '__main__':
    start_http_server(1006)
    while True:
        temperature_gauge.set(sensor.temperature)
        humidity_gauge.set(sensor.relative_humidity)

        time.sleep(int(TIME_BETWEEN_READINGS))
