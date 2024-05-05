""" Validate Prometheus metrics for a given label and value pair. """

from datetime import datetime, timedelta
import logging
import os
import requests

# Set up logging
logging.basicConfig(level=logging.INFO)

# Environment variables for Prometheus
endpoint = os.environ.get('METRICSURE_ENDPOINT')
metric = os.environ.get('METRICSURE_METRIC')
label = os.environ.get('METRICSURE_LABEL')
values = os.environ.get('METRICSURE_VALUES', '')

# Environment variables for Netbox
netbox_endpoint = os.environ.get('METRICSURE_NETBOX_ENDPOINT')
netbox_token = os.environ.get('METRICSURE_NETBOX_TOKEN')

def query_prometheus(endpoint, metric, label, label_value):
    """ Query Prometheus for a given metric with a label and value pair. """
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=1)
    start_str = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    end_str = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    query = f'{metric}{{{label}="{label_value}"}}'
    url = f'{endpoint}/api/v1/query_range?query={query}&start={start_str}&end={end_str}&step=1m'
    response = requests.get(url)
    if 'result' in response.json()['data'] and response.json()['data']['result'] and 'values' in response.json()['data']['result'][0]:
        logging.info(f'Metric {metric} with {label}="{label_value}" exists in the last 24 hours.')
        return True
    else:
        logging.error(f'Metric {metric} with {label}="{label_value}" not found in the last 24 hours.')
        return False

def get_netbox_devices(netbox_endpoint, netbox_token):
    if not netbox_endpoint or not netbox_token:
        logging.info("Netbox URL or token not provided. Skipping Netbox device retrieval.")
        return []

    headers = {'Authorization': f'Token {netbox_token}'}
    url = f'{netbox_endpoint}/api/dcim/devices/?status=active'
    logging.info(f"Requesting URL: {url}")
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            devices = response.json()
            return [device['name'] for device in devices['results']] if 'results' in devices else []
        except ValueError as e:
            logging.error(f"Failed to decode JSON from response: {response.text}")
            return []
    else:
        logging.error(f"HTTP Error {response.status_code}: {response.text}")
        return []


# Optional: Retrieve devices only if Netbox credentials are provided
if netbox_endpoint and netbox_token:
    devices = get_netbox_devices(netbox_endpoint, netbox_token)
else:
    devices = []

# Adjusted Prometheus queries to include devices from Netbox
label_values = [value.strip() for value in values.split(',') if value.strip()]
if not label_values:  # If no values are specified, use Netbox devices
    label_values = devices

label_value_pair_with_no_metrics = []
for label_value in label_values:
    if not query_prometheus(endpoint, metric, label, label_value):
        label_value_pair_with_no_metrics.append(label_value)

if label_value_pair_with_no_metrics:
    invalid_values = ','.join(label_value_pair_with_no_metrics)
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        print(f'invalid_values={invalid_values}', file=fh)
else:
    print("All instances have metrics in the last 24 hours.")
