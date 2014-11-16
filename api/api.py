import requests


class API:
    """A base class for making api requests"""
    def __init__(self, url, key):
        self.url = url
        self.__key = key

    def get(self, endpoint, params=None):
        api_endpoint = self.url + '/' + endpoint
        params = {} if params is None else params
        params['key'] = self.__key

        results = requests.get(api_endpoint, params=params)

        if results.status_code == requests.codes.ok:
            return results
        else:
            # throw an error
            results.raise_for_status()

    def get_json(self, endpoint, params=None):
        results = self.get(endpoint, params)

        if results.raise_for_status() is None:
            return results.json()
