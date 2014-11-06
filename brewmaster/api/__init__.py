import requests


class API:
    """An API Base Class for making api requests"""
    def __init__(self, url, key):
        self.url = url
        self.__key = key

    def get(self, endpoint, params):
        api_endpoint = self.url + "/" + endpoint
        params["key"] = self.__key

        results = requests.get(api_endpoint, params=params)

        if results.status_code == requests.codes.ok:
            return results
        else:
            # TODO: need a better solution here
            # throw an error
            print "There was an error"

    def get_json(self, endpoint, params):
        results = self.get(endpoint, params)

        if results.status_code == requests.codes.ok:
            return results.json()
