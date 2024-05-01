[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/badges/StandWithUkraine.svg)](https://stand-with-ukraine.pp.ua)
[![Test metricsure](https://github.com/LukoJy3D/metricsure/actions/workflows/ci.yml/badge.svg)](https://github.com/LukoJy3D/metricsure/actions/workflows/ci.yml)
[![Star on GitHub](https://img.shields.io/github/stars/LukoJy3D/metricsure.svg?style=social)](https://github.com/LukoJy3D/metricsure/stargazers)


# metricsure

Simple github action to validate metric existence with specific labels and values against prometheus like endpoint.

## Inputs

- `endpoint` - Prometheus like endpoint to query metrics from.
- `metric` - Metric name to query. (Currently only supports single metric)
- `label` - Label name to query. (Currently only supports single label)
- `values` - Label values to query.

## Outputs

`invalid_values` - List of values that did not return any metrics from the endpoint.
