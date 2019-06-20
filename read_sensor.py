import os
import time
from collections import deque
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

temperatures = deque()
humidities = deque()


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
        temperatures.appendleft(sensor.temperature)
        humidities.appendleft(sensor.relative_humidity)
        tmp_temperature = sensor.temperature
        tmp_humidity = sensor.relative_humidity

        if len(temperatures) > 5:
            temperatures.pop()
            tmp_temperatures = list(temperatures)

            # Remove min/max values
            tmp_temperatures.remove(max(tmp_temperatures))
            tmp_temperatures.remove(min(tmp_temperatures))

            # Report the average
            tmp_temperature = sum(tmp_temperatures)/len(tmp_temperatures)

        if len(humidities) > 5:
            humidities.pop()
            tmp_humidities = list(humidities)

            # Remove min/max values
            tmp_humidities.remove(max(tmp_humidities))
            tmp_humidities.remove(min(tmp_humidities))

            # Report the average
            tmp_humidity = sum(tmp_humidities)/len(tmp_humidities)

        temperature_gauge.set(tmp_temperature)
        humidity_gauge.set(tmp_humidity)

        time.sleep(int(TIME_BETWEEN_READINGS))
