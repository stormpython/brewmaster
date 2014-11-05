import requests


class API:
    """API Base Class"""
    def __init__(self, url, key):
        self.url = url
        self.__key = key

    def get(self, endpoint, params):
        api_endpoint = self.url + '/' + endpoint
        params['key'] = self.__key

        results = requests.get(api_endpoint, params=params)

        if results.status_code == 200:
            return results
        else:
            # TODO: need a better solution here
            print 'There was an error'
