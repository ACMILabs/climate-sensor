import os
import time
from collections import deque

import Adafruit_DHT
from prometheus_client import Gauge, start_http_server

DEBUG = os.getenv('DEBUG', 'false') == 'true'
SENSOR_PIN = int(os.getenv('SENSOR_PIN', '4'))
TIME_BETWEEN_READINGS = os.getenv('TIME_BETWEEN_READINGS')

TEMPERATURES = deque()
HUMIDITIES = deque()
SENSOR = Adafruit_DHT.DHT22
TEMPERATURE_GAUGE = Gauge('ambient_temperature', 'Ambient temperature')
HUMIDITY_GAUGE = Gauge('ambient_humidity', 'Ambient humidity')
SET_AVERAGE_READINGS = os.getenv('SET_AVERAGE_READINGS', 'true') == 'true'


def set_average_readings(temperature, humidity, set_average=True):
    """
    Sets the temperature and humidity gauges with the average of the last 5 readings
    when more than 5 readings have been made.
    The function drops the minimum and maximum values, and averages the remaining.
    """

    try:
        if 0 <= humidity <= 100:
            if set_average:
                TEMPERATURES.appendleft(temperature)
                HUMIDITIES.appendleft(humidity)
                average_temperature = temperature
                average_humidity = humidity

                if len(TEMPERATURES) > 5:
                    TEMPERATURES.pop()
                    tmp_temperatures = list(TEMPERATURES)

                    # Remove min/max values
                    tmp_temperatures.remove(max(tmp_temperatures))
                    tmp_temperatures.remove(min(tmp_temperatures))

                    # Get the average
                    average_temperature = sum(tmp_temperatures)/len(tmp_temperatures)

                if len(HUMIDITIES) > 5:
                    HUMIDITIES.pop()
                    tmp_humidities = list(HUMIDITIES)

                    # Remove min/max values
                    tmp_humidities.remove(max(tmp_humidities))
                    tmp_humidities.remove(min(tmp_humidities))

                    # Get the average
                    average_humidity = sum(tmp_humidities)/len(tmp_humidities)

                TEMPERATURE_GAUGE.set(average_temperature)
                HUMIDITY_GAUGE.set(average_humidity)
            else:
                TEMPERATURE_GAUGE.set(temperature)
                HUMIDITY_GAUGE.set(humidity)
        else:
            if DEBUG:
                print(f'Ignoring reading outside expected range: {temperature}°C, {humidity}%')
    except TypeError:
        if DEBUG:
            print(f'Ignoring bad reading: {temperature}°C, {humidity}%')


if __name__ == '__main__':
    start_http_server(1006)
    while True:
        try:
            HUMIDITY, TEMPERATURE = Adafruit_DHT.read_retry(SENSOR, SENSOR_PIN)
            set_average_readings(TEMPERATURE, HUMIDITY, SET_AVERAGE_READINGS)
        except (ImportError, RuntimeError) as exception:
            TEMPLATE = 'An exception of type {0} occurred. Arguments:\n{1!r}'
            MESSAGE = TEMPLATE.format(type(exception).__name__, exception.args)
            if DEBUG:
                print(MESSAGE)

        time.sleep(int(TIME_BETWEEN_READINGS))
