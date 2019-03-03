#!/bin/bash

git clone https://github.com/adafruit/Adafruit_Python_DHT.git && cd Adafruit_Python_DHT && python setup.py install
python read_sensor.py
