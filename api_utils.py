import json
import requests
from requests.utils import urlparse
import logging
from json import loads

def send_post_request(url, data, headers=None, timeout=10):
    try:
        response = requests.post(url, json=data, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"POST request failed: {e}")
        return None

def send_get_request(url, params=None, headers=None, timeout=10):
    try:
        response = requests.get(url, params=params, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"GET request failed: {e}")
        return None

def validate_api_key(api_key):
    return isinstance(api_key, str) and len(api_key) > 0


def validate_url(url):
    try:
        result = requests.utils.urlparse(url)  # type: ignore
        return all([result.scheme, result.netloc])
    except Exception as e:
        logging.error(f"URL validation failed: {e}")
        return False


def is_valid_json(json_string):
    try:
        json.loads(json_string)
        return True
    except ValueError as e:
        logging.error(f"Invalid JSON: {e}")
        return False

