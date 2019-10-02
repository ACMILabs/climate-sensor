import os
import time
from collections import deque
from datetime import datetime

import Adafruit_DHT
import pytz
from prometheus_client import Gauge, start_http_server

TIME_BETWEEN_READINGS = os.getenv('TIME_BETWEEN_READINGS')
TIMEZONE = os.getenv('TIMEZONE', 'Australia/Melbourne')
TEMPERATURES = deque()
HUMIDITIES = deque()


def datetime_now():
    pytz_timezone = pytz.timezone(TIMEZONE)
    return datetime.now(pytz_timezone).isoformat()


SENSOR = Adafruit_DHT.DHT22
PIN = 4
TEMPERATURE_GAUGE = Gauge('ambient_temperature', 'Ambient temperature')
HUMIDITY_GAUGE = Gauge('ambient_humidity', 'Ambient humidity')

if __name__ == '__main__':
    start_http_server(1006)
    while True:
        try:
            HUMIDITY, TEMPERATURE = Adafruit_DHT.read_retry(SENSOR, PIN)
        except (ImportError, RuntimeError) as exception:
            TEMPLATE = 'An exception of type {0} occurred. Arguments:\n{1!r}'
            MESSAGE = TEMPLATE.format(type(exception).__name__, exception.args)
            print(MESSAGE)

            # Set default values for tests/failed reads.
            HUMIDITY = 1
            TEMPERATURE = 1

        if HUMIDITY < 0 or HUMIDITY > 100:
            continue

        TEMPERATURES.appendleft(TEMPERATURE)
        HUMIDITIES.appendleft(HUMIDITY)
        TMP_TEMPERATURE = TEMPERATURE
        TMP_HUMIDITY = HUMIDITY

        if len(TEMPERATURES) > 5:
            TEMPERATURES.pop()
            TMP_TEMPERATURES = list(TEMPERATURES)

            # Remove min/max values
            TMP_TEMPERATURES.remove(max(TMP_TEMPERATURES))
            TMP_TEMPERATURES.remove(min(TMP_TEMPERATURES))

            # Report the average
            TMP_TEMPERATURE = sum(TMP_TEMPERATURES)/len(TMP_TEMPERATURES)

        if len(HUMIDITIES) > 5:
            HUMIDITIES.pop()
            TMP_HUMIDITIES = list(HUMIDITIES)

            # Remove min/max values
            TMP_HUMIDITIES.remove(max(TMP_HUMIDITIES))
            TMP_HUMIDITIES.remove(min(TMP_HUMIDITIES))

            # Report the average
            TMP_HUMIDITY = sum(TMP_HUMIDITIES)/len(TMP_HUMIDITIES)

        TEMPERATURE_GAUGE.set(TMP_TEMPERATURE)
        HUMIDITY_GAUGE.set(TMP_HUMIDITY)

        time.sleep(int(TIME_BETWEEN_READINGS))
