from api import API
from app import app
from brewmaster.database import save_beer


url = app.config['BREWERY_DB_API_URL']
key = app.config['BREWERY_DB_API_KEY']


class BreweryDBApi(API):

    def __init__(self):
        API.__init__(self, url, key)
        self.beer_not_found = app.config['NO_BEER_FOUND']

    def call_api(self, endpoint, params):
        results = self.get(endpoint, params).json()

        if 'data' in results:
            return results['data']
        else:
            return self.beer_not_found

    def call_beer_api_endpoint(self, search_term, is_id):
        params = {}

        if is_id is True:
            endpoint = 'beer/' + search_term
        else:
            endpoint = 'beers'
            params['name'] = search_term

        results = self.call_api(endpoint, params)

        if len(results) == 1 or isinstance(results, dict):
            beer = results[0] if len(results) == 1 else results
            save_beer(beer)
            return beer
        else:
            return self.beer_not_found
