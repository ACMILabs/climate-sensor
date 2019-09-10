# Temperature and Humidity sensor prototype

A Raspberry Pi with a [DFRobot DHT22 v2 sensor](https://core-electronics.com.au/dht22-temperature-and-humidity-sensor.html) to measure temperature and humidity.

## Monitoring & Graphing

There's a [Prometheus](https://prometheus.io) [client](https://github.com/prometheus/client_python) in `read_sensors.py` that exports the climate data.

We use a [Graphana](https://grafana.com) dashboard to view the data.

## Deploying via Balena Cloud

Clone this repo and make any edits to `read_sensors.py` that you need.

Add the Balena remote to:

```bash
git remote add balena <username>@git.balena-cloud.com:<username>/<balena-app-name>.git
```

And then push the changes to deploy via Balena:

```bash
$ git commit -S -am ...
$ git push
$ git push balena master
```

Watch the devices update on the [Balena dashboard](https://dashboard.balena-cloud.com).

## Credits

This project was built by the [ACMILabs](https://labs.acmi.net.au) team in 2019.

[MIT License](LICENSE)
