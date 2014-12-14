from api import API
from app import app
from brewmaster.database import save_beer


url = app.config['BREWERY_DB_API_URL']
key = app.config['BREWERY_DB_API_KEY']


class BreweryDB(API):
    """An API request class for BreweryDb"""
    def __init__(self):
        API.__init__(self, url, key)
        self.beer_not_found = app.config['NO_BEER_FOUND']

    def call_api(self, endpoint, params):
        """Makes an API request to a specified endpoint"""
        results = self.get_json(endpoint, params)

        if 'data' in results:
            return results
        else:
            return self.beer_not_found

    def get_beer(self, search_term, is_id):
        """Returns a dictionary of beer attributes if beer is present in the
        BreweryDB database.
        """
        params = {}

        # Determine which BreweryDB endpoint to use
        if is_id is True:
            endpoint = 'beer/' + search_term
        else:
            endpoint = 'beers'
            params['name'] = search_term

        # Make BreweryDB API request
        results = self.call_api(endpoint, params)

        # Save dictionary of beer attributes to the MySQL database and return
        # to user if beer is present. Else return the results from the API
        # request.

        # If results['data'], results['data'] could be an array of dictionaries
        # if using the `beers` endpoint or a dictionary if using the
        # `beer/<beer_id>` endpoint.
        if 'data' in results and len(results['data']) == 1 \
                or 'data' in results and isinstance(results['data'], dict):
            beer = results['data'][0] if len(results['data']) == 1 \
                else results['data']
            save_beer(beer)
            return beer
        else:
            return results
