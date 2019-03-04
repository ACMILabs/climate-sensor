# Temperature and Humidity sensor prototype

A Raspberry Pi with a [DFRobot DHT22 v2 sensor](https://core-electronics.com.au/dht22-temperature-and-humidity-sensor.html) to measure temperature and humidity.

## Deploying via Balena Cloud

Clone this repo and make any edits to `read_sensors.py` that you need.

Add the Balena remote to:

```bash
git remote add balena g_acmi_developer@git.balena-cloud.com:g_acmi_developer/temperature-humidity.git
```

And then push the changes to deploy:

```bash
git push
git push balena master
```

Watch the devices update on the [Balena dashboard](https://dashboard.balena-cloud.com/apps/1399290/devices).
