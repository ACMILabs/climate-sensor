import os, time
from datetime import datetime

import Adafruit_DHT
import pytz
import requests
from prometheus_client import Gauge, start_http_server


# Constants
LOCATION_NAME = os.getenv('LOCATION_NAME')
LOCATION_DESCRIPTION = os.getenv('LOCATION_DESCRIPTION')
XOS_CLIMATE_STATUS_ENDPOINT = os.getenv('XOS_CLIMATE_STATUS_ENDPOINT')
TIME_BETWEEN_READINGS = os.getenv('TIME_BETWEEN_READINGS')


def datetime_now():
    pytz_timezone = pytz.timezone('Australia/Melbourne')
    return datetime.now(pytz_timezone).isoformat()

sensor = Adafruit_DHT.DHT22
pin = 4
temperature_gauge = Gauge('ambient_temperature', 'Ambient temperature')
humidity_gauge = Gauge('ambient_humidity', 'Ambient humidity')

if __name__ == '__main__':
    start_http_server(1006)
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        temperature_gauge.set(temperature)
        humidity_gauge.set(humidity)

        time.sleep(int(TIME_BETWEEN_READINGS))
