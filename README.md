[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

## HA-Buienradar-Precipitation-Forecast
Home Assistent integration to fetch the (2h) precipitation forecast from Buienradar (NL).

## Installation
(1) Install as a custom integration using HACS [(see this guide)](https://hacs.xyz/docs/faq/custom_repositories).

(2) For a manual install:
- download the integration from the [latest release](https://github.com/DennisB66/HA-Buienradar-Precipitation-Forecast/releases/).
- copy the `Buienradar_2h_Forecast` directory into your /config/custom_components directory.
- restart HA.

In your HA installation the following should exist:
```text
custom_components/buienradar_2h_forecast/__init__.py
custom_components/buienradar_2h_forecast/manifest.json
custom_components/buienradar_2h_forecast/sensor.py
```

In your Home Assistent UI go to "Settings/Devices & Services/Integrations", click "ADD INTEGRATION" and select "Buienradar_2h_Forecast". Default values for the config parameters will be populated in the config window. Change any paramter if needed and click "SUBMIT".

Note: Addtional sensors (for other locationa) can be added with "ADD ENTRY" in the integration screen.

## Config Parameters
| Paramter        | Values         | Description                                                   |
| --------------- | -------------- | ------------------------------------------------------------- |
| `Name`          | string         | Location name of the sensor (default "home")                  |
| `latitude`      | number         | Latitude coordinate of the forecast requested                 |
| `longitude`     | number         | Longitude coordinate of the forecast requested                |

Note: the default values for latitude and longitude, if not provided, are taken from the Home Assistant settings.

## Sensor Attributes
| Attribute       | Values         | Description                                                   |
| --------------- | -------------- | ------------------------------------------------------------- |
| `state`         | number         | Total expected precipitation (in mm) in the coming 2 hours    |
| `forecast`      | json array     | Expected Precipitation (in mm) for every 5 minutes            |

## Example of usage
The forecast can be visualized using the [`custom:apexcharts-card`](https://github.com/RomRider/apexcharts-card):

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
  title: Buienradar 2h Forecast
  show: true
  show_states: true
  colorize_states: false
hours_12: false
now:
  show: true
  label: now
series:
  - entity: sensor.sensor.buienradar_2h_forecast_home
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