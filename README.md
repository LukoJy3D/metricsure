[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/badges/StandWithUkraine.svg)](https://stand-with-ukraine.pp.ua)
[![Test metricsure](https://github.com/LukoJy3D/metricsure/actions/workflows/ci.yml/badge.svg)](https://github.com/LukoJy3D/metricsure/actions/workflows/ci.yml)
[![Star on GitHub](https://img.shields.io/github/stars/LukoJy3D/metricsure.svg?style=social)](https://github.com/LukoJy3D/metricsure/stargazers)

# metricsure

Simple github action to validate metric existence with specific labels and values against prometheus like endpoint. Supports querying device names from netbox.

## Inputs

- `endpoint` - Prometheus like endpoint to query metrics from.
- `metric` - Metric name to query. (Currently only supports single metric)
- `label` - Label name to query. (Currently only supports single label)
- `values` - Label values to query.
- `netbox_endpoint` - Netbox endpoint to query for device names.
- `netbox_token` - Netbox token to authenticate with.

## Outputs

`invalid_values` - List of values that did not return any metrics from the endpoint.

## Example usage

Most of examples can be found in the [test workflow](.github/workflows/test.yml). However since netbox demo is not persistent, tests can not be written for it, so here is the simple example of how to do it with token:

```yaml
name: Validate metrics

on:
  schedule:
    - cron: "0 0 * * *"

jobs:
  test-netbox:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Run metricsure
        id: metricsure
        uses: lukojy3d/metricsure@main
        with:
          endpoint: "https://prometheus.demo.do.prometheus.io"
          metric: "ipmi_dcmi_power_consumption_watts"
          label: "instance"
          netbox_endpoint: "https://demo.netbox.dev"
          netbox_token: "{{ secrets.NETBOX_TOKEN }}"

      - name: List all returned values
        run: echo ${{ steps.metricsure.outputs.invalid_values }}
```
