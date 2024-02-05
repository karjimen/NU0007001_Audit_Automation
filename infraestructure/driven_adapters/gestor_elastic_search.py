import datetime
import requests
import json

from domain.utils import constants


class ElasticSearchIntegration:

    def __init__(self, url_endpoint, user, password):
        self.url_endpoint = url_endpoint
        self.user = user
        self.password = password

    def set_max_result_window(self, limit_index):
        payload = {
            "index.max_result_window": limit_index,
        }

        headers = {
            'cache-control': 'no-cache',
            'Content-Type': 'application/json'
        }

        data = json.dumps(payload)
        session = requests.Session()
        session.trust_env = False
        response = session.request("PUT", self.url_endpoint, headers=headers, data=data)
        return response.status_code


    def get_info_index(self, limit_index, sources):
        payload = {
            "_source": sources,
            "size": limit_index
        }

        headers = {
            'cache-control': 'no-cache',
            'Content-Type': 'application/json'
        }

        data = json.dumps(payload)
        session = requests.Session()
        session.trust_env = False
        response = session.request("GET", self.url_endpoint, headers=headers, data=data, verify=False)
        return response.json()

    def get_info_index_with_payload(self, payload_input):
        payload = payload_input

        headers = {
            'cache-control': 'no-cache',
            'Content-Type': 'application/json'
        }

        data = json.dumps(payload)
        session = requests.Session()
        session.trust_env = False
        response = session.request("GET", self.url_endpoint, headers=headers, data=data, verify=False)
        return response.json()

