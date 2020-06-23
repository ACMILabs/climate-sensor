Climate Sensor
==============

A Raspberry Pi with a DFRobot DHT22 sensor to measure temperature and humidity and export that data to a monitoring and graphing server.

## Features

* Measures Temperature in Celcius °C
* Measures Humidity in Relative Humidity %
* Exposes the climate sensor data on an http server on port `1006` e.g. [http://<ip_address>:1006](http://<ip_address>:1006)
* Compatible with [Prometheus](https://prometheus.io)

![Climate Sensor](images/climate-sensor.jpg)

## Monitoring & Graphing

There's a [Prometheus](https://prometheus.io) [client](https://github.com/prometheus/client_python) in `read_sensors.py` that exports the climate data.

We use a [Graphana](https://grafana.com) dashboard to view the data.

## Hardware

This Climate Sensor is designed to run with the following hardware:

* [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/)
* [DFRobot DHT22 v2 sensor](https://www.dfrobot.com/product-1102.html)
* [JST PH 3-Pin to Female Socket Cable](https://core-electronics.com.au/jst-ph-3-pin-to-female-socket-cable-200mm.html)

**Note**: It will run on any model of Raspberry Pi, but for conservation of electricity and minimising heat production we recommend the Zero.

## Wiring diagram

With your Raspberry Pi pins on the right-hand side of the board, using the pin numbering system in the following diagram, attach the DHT22 cables to the Raspberry Pi pins in the table below:

| Raspberry Pi pin | DFRobot DHT22 pin |
| - | - |
| 1 - 3V3 Power | Red power cable |
| 7 - RPI04 | Green/White data cable |
| 9 - Ground | Black ground cable |

![Raspberry Pi Zero pinout](images/raspberry-pi-zero.png)

## Deploying via Balena Cloud

Clone this repo and make any edits to `read_sensors.py` that you need.

Add the Balena remote to:

```bash
git remote add balena <username>@git.balena-cloud.com:<username>/<balena-app-name>.git
```

And then push the changes to deploy via Balena:

```bash
$ git commit -S -am "My new feature"
$ git push
$ git push balena master
```

Watch the devices update on the [Balena dashboard](https://dashboard.balena-cloud.com).

## Credits

This project was built by the [ACMILabs](https://labs.acmi.net.au) team in 2019.

[MIT License](LICENSE)
