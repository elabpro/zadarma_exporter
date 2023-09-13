#!/usr/bin/env python3

import os
import re
import platform
import time
import yaml
import api
import json

from http.server import BaseHTTPRequestHandler, HTTPServer

from prometheus_client import start_http_server, Summary, Gauge, Histogram

config_file = "/app/config.yml"

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
balance = Gauge('zadarma_balance_total', 'Current balance on Zadarma')

# Decorate function with metric.
@REQUEST_TIME.time()
def process_request(config):
    """ Connect to Zadarma """
    z_api = api.ZadarmaAPI(key=config['key'], secret=config['secret'])
    b = json.loads(z_api.call('/v1/info/balance//v1/info/balance/'))
    balance.set(b['balance'])
    

if __name__ == '__main__':
    app_config = {
        "app": {"port": 9000},
        "zadarma": {"key": "", "secret": ""}
    }
    with open(config_file, "r") as config:
        app_config = yaml.load(config, Loader=yaml.FullLoader)
    start_http_server(app_config["app"]["port"])
    #request_counter = Counter('http_requests', 'HTTP request', ["status_code", "instance"])

    while True:
        process_request(app_config['zadarma'])
        time.sleep(app_config['app']['delay'])
