from collections import deque

import read_sensor


def reset_sensor():
    """
    Reset the read_sensor values.
    """

    read_sensor.TEMPERATURES = deque()
    read_sensor.HUMIDITIES = deque()
    read_sensor.TEMPERATURE_GAUGE.set(0)
    read_sensor.HUMIDITY_GAUGE.set(0)


def test_set_average_readings():
    """
    Test that set_average_readings sets the gauges with expected results.
    """

    read_sensor.TEMPERATURES.appendleft(10)
    read_sensor.TEMPERATURES.appendleft(20)
    read_sensor.TEMPERATURES.appendleft(30)
    read_sensor.TEMPERATURES.appendleft(40)
    read_sensor.TEMPERATURES.appendleft(50)
    read_sensor.HUMIDITIES.appendleft(35)
    read_sensor.HUMIDITIES.appendleft(45)
    read_sensor.HUMIDITIES.appendleft(55)
    read_sensor.HUMIDITIES.appendleft(65)
    read_sensor.HUMIDITIES.appendleft(75)

    temperature = 21.5
    humidity = 54
    read_sensor.set_average_readings(temperature, humidity)

    assert read_sensor.TEMPERATURE_GAUGE.collect()[0].samples[0].value == 30.5
    assert read_sensor.HUMIDITY_GAUGE.collect()[0].samples[0].value == 58
    assert temperature in list(read_sensor.TEMPERATURES)
    assert humidity in list(read_sensor.HUMIDITIES)

    # Test with set_average set to False
    read_sensor.set_average_readings(temperature, humidity, set_average=False)
    assert read_sensor.TEMPERATURE_GAUGE.collect()[0].samples[0].value == 21.5
    assert read_sensor.HUMIDITY_GAUGE.collect()[0].samples[0].value == 54


def test_set_average_readings_with_first_reading():
    """
    Test the first set_average_readings call returns the initial readings.
    """

    reset_sensor()
    temperature = 21.5
    humidity = 54
    read_sensor.set_average_readings(temperature, humidity)

    assert read_sensor.TEMPERATURE_GAUGE.collect()[0].samples[0].value == 21.5
    assert read_sensor.HUMIDITY_GAUGE.collect()[0].samples[0].value == 54
    assert temperature in list(read_sensor.TEMPERATURES)
    assert humidity in list(read_sensor.HUMIDITIES)


def test_set_average_readings_with_bad_values():
    """
    Test that set_average_readings ignores bad values and doesn't store or set those values.
    """

    reset_sensor()
    initial_temperatures = read_sensor.TEMPERATURES
    initial_temperature_gauge = read_sensor.TEMPERATURE_GAUGE.collect()[0].samples[0].value
    initial_humidities = read_sensor.HUMIDITIES
    initial_humidity_gauge = read_sensor.HUMIDITY_GAUGE.collect()[0].samples[0].value
    temperature = -666
    humidity = 666
    read_sensor.set_average_readings(temperature, humidity)

    assert initial_temperatures == read_sensor.TEMPERATURES
    assert temperature not in list(read_sensor.TEMPERATURES)
    assert initial_temperature_gauge == read_sensor.TEMPERATURE_GAUGE.collect()[0].samples[0].value
    assert initial_humidities == read_sensor.HUMIDITIES
    assert humidity not in list(read_sensor.HUMIDITIES)
    assert initial_humidity_gauge == read_sensor.HUMIDITY_GAUGE.collect()[0].samples[0].value


def test_set_average_readings_with_none():
    """
    Test that set_average_readings handles None values and doesn't try to store or set them.
    """

    reset_sensor()
    temperature = None
    humidity = None
    read_sensor.set_average_readings(temperature, humidity)

    assert read_sensor.TEMPERATURE_GAUGE.collect()[0].samples[0].value == 0
    assert read_sensor.HUMIDITY_GAUGE.collect()[0].samples[0].value == 0
    assert temperature not in list(read_sensor.TEMPERATURES)
    assert humidity not in list(read_sensor.HUMIDITIES)
