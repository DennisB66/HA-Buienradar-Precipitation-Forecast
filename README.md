[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

## HA-Buienradar-Precipitation-Forecast
Home Assistent integration to fetch the (2h) precipitation forecast from Buienradar (NL).

## Installation
Install as a custom integration using HACS [(see this guide)](https://hacs.xyz/docs/faq/custom_repositoriess).

For a manual install:
- download the integration from the [latest release](https://github.com/DennisB66/HA-Buienradar-Precipitation-Forecast/releases/).
- copy the `Buienradar-Precipitation-Forecast` directory into your /config/custom_components directory.
- restart HA.


In your HA installation you should now also have this:
```text
custom_components/buienradar_precipitation_forecast/__init__.py
custom_components/buienradar_precipitation_forecast/manifest.json
custom_components/buienradar_precipitation_forecast/sensor.py
```

## Configuration
Add the following to your configuration.yaml file and restart Home Assistant:
```yaml
sensor:
  - platform: buienradar_precipitation_forecast
    latitude: 51.000  # replace with your coordinate
    longitude: 3.000  # replace with your coordinate
```

## Sensor Parameters
| Option          | Values         | Description                                                   | default  |
| --------------- | -------------- | ------------------------------------------------------------- | -------- |
| `latitude`      | number         | Latitude coordinate of the forecast requested                 |  51.00   |
| `longitude`     | number         | Longitude coordinate of the forecast requested                |  3.000   |

## Sensor Attributes
| Attribute       | Values         | Description                                                   |
| --------------- | -------------- | ------------------------------------------------------------- |
| `state`         | number         | Total expected precipitation (in mm) in the coming 2 hours    |
| `forecast`      | json array     | Expected Precipitation (in mm) for every 5 minutes            |

## Example of usage
The forecart can be visualized using the [`custom:apexcharts-card`](https://github.com/RomRider/apexcharts-card):

![apexcharts-card](https://raw.githubusercontent.com/DennisB66/HA-Buienradar-Precipitation-Forecast/main/media/apexcharts-card.png)

Example of `apexcharts-card` configuration:
```yaml
type: custom:apexcharts-card
graph_span: 120min
span:
  start: minute
apex_config:
  chart:
    height: 300px
  dataLabels:
    enabled: true
header:
  title: Buienradar Precipitation Forecast
  show: true
  show_states: true
  colorize_states: false
hours_12: false
now:
  show: true
  label: now
series:
  - entity: sensor.buienradar_precipitation_forecast
    name: total (2h)
    type: column
    color: blue
    show:
      in_header: raw
      name_in_header: false
      extremas: true
    data_generator: |
      return entity.attributes.forecast.map(entry => {
        return [new Date(entry.time), entry.rain];
      });
```
Example of `forecast` data:
```
forecast:
  - time: '2022-04-09T08:45:00'
    rain: 0.02
  - time: '2022-04-09T08:50:00'
    rain: 0.08
  - time: '2022-04-09T08:55:00'
    rain: 0.02
  - time: '2022-04-09T09:00:00'
    rain: 0
  - time: '2022-04-09T09:05:00'
    rain: 0.04
  - time: '2022-04-09T09:10:00'
    rain: 0.02
  - time: '2022-04-09T09:15:00'
    rain: 0.04
  - time: '2022-04-09T09:20:00'
    rain: 0.04
  - time: '2022-04-09T09:25:00'
    rain: 0.08
  - time: '2022-04-09T09:30:00'
    rain: 0.25
  - time: '2022-04-09T09:35:00'
    rain: 1.03
  - time: '2022-04-09T09:40:00'
    rain: 0.67
  - time: '2022-04-09T09:45:00'
    rain: 0.44
  - time: '2022-04-09T09:50:00'
    rain: 0
  - time: '2022-04-09T09:55:00'
    rain: 0
  - time: '2022-04-09T10:00:00'
    rain: 0
  - time: '2022-04-09T10:05:00'
    rain: 0.01
  - time: '2022-04-09T10:10:00'
    rain: 0
  - time: '2022-04-09T10:15:00'
    rain: 0
  - time: '2022-04-09T10:20:00'
    rain: 0
  - time: '2022-04-09T10:25:00'
    rain: 0
  - time: '2022-04-09T10:30:00'
    rain: 0
  - time: '2022-04-09T10:35:00'
    rain: 0
  - time: '2022-04-09T10:40:00'
    rain: 0
```