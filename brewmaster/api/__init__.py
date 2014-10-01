import requests
import os


class API:
    """API Base Class"""
    def __init__(self, url, key):
        self.url = url
        self.__key = key

    def call_api(self, endpoint, params):
        api_endpoint = self.url + '/' + endpoint
        params['key'] = self.__key

        results = requests.get(api_endpoint, params=params)

        if results.status_code == 200:
            return results
        else:
            # TODO: need a better solution here
            print 'There was an error'


class BrewerydbAPI(API):
    """BreweryDB API Class"""
    def __init__(self):
        url = 'http://api.brewerydb.com/v2'
        key = os.environ.get('BREWERY_DB_API_KEY')

        API.__init__(self, url, key)
