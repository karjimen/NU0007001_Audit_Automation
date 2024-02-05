import datetime
import requests
import json

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class ElasticSearchIntegration:

    def __init__(self, url_endpoint, password, user):
        self.__url_endpoint = url_endpoint
        self.__password = password
        self.__user = user

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
        response = session.request("PUT", self.__url_endpoint, headers=headers, data=data)
        return response.status_code


    def update_index_by_query(self, payload):

        headers = {
            'cache-control': 'no-cache',
            'Content-Type': 'application/json'
        }

        data = json.dumps(payload)
        try:
            session = requests.Session()
            session.trust_env = False
            response = session.post(
                url=self.__url_endpoint,
                data=data,
                verify=False,
                headers=headers,
                timeout=20.0
            )

            return response

        except requests.exceptions.Timeout as e:
            print(f"Timeout Error update index: payload={payload}: {e} ")
            raise SystemExit(e)
        except requests.exceptions.TooManyRedirects as e:
            print(f"TooManyRedirects Error update index: payload={payload}: {e}")
            raise SystemExit(e)
        except requests.exceptions.RequestException as e:
            print(f"RequestException Error update index: payload={payload}: {e}")
            raise SystemExit(e)