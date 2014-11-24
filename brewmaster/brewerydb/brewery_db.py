from api import API
from app import app
from brewmaster.database import save_beer


url = app.config['BREWERY_DB_API_URL']
key = app.config['BREWERY_DB_API_KEY']


class BreweryDB(API):

    def __init__(self):
        API.__init__(self, url, key)
        self.beer_not_found = app.config['NO_BEER_FOUND']

    def call_api(self, endpoint, params):
        results = self.get_json(endpoint, params)

        if 'data' in results:
            return results
        else:
            return self.beer_not_found

    def get_beer(self, search_term, is_id):
        params = {}

        if is_id is True:
            endpoint = 'beer/' + search_term
        else:
            endpoint = 'beers'
            params['name'] = search_term

        results = self.call_api(endpoint, params)

        if 'data' in results and len(results['data']) == 1 \
                or 'data' in results and isinstance(results['data'], dict):
            beer = results['data'][0] if len(results['data']) == 1 \
                else results['data']
            save_beer(beer)
            return beer
        else:
            return self.beer_not_found
