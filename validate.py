import requests
from datetime import datetime, timedelta
import logging
import os

endpoint = os.environ.get('ENDPOINT')
metric = os.environ.get('METRIC')
label = os.environ.get('LABEL')
values = os.environ.get('VALUES', '')

def query_prometheus(endpoint, metric, label, label_value):
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

label_values = [value.strip() for value in values.split(',') if value.strip()]
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
