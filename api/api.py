import requests


class API:
    """An API Base Class for making api requests"""
    def __init__(self, url, key):
        self.url = url
        self.__key = key

    def get(self, endpoint, params=None):
        api_endpoint = self.url + '/' + endpoint
        params = {} if params is None else params
        params['key'] = self.__key

        try:
            results = requests.get(api_endpoint, params=params)

            if results.status_code == requests.codes.ok:
                return results
        except requests.exceptions.RequestException as e:
            print e

    def get_json(self, endpoint, params):
        results = self.get(endpoint, params)

        if results.raise_for_status() is None:
            return results.json()
