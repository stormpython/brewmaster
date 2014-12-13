from app import app
from database import lookup_beer
from brewerydb import BreweryDB


class BrewMaster:
    """Main algorithm for the BrewMaster application"""
    def __init__(self, search_term, is_id=False, page=1):
        self.search_term = search_term
        self.is_id = is_id
        self.page = page

        # API settings
        self.brewery_db = BreweryDB()
        self.name_endpoint = 'beers'
        self.search_endpoint = 'search'

        # Not found response
        self.beer_not_found = app.config['NO_BEER_FOUND']
        self.similar_beers_not_found = app.config['SIMILAR_BEERS_NOT_FOUND']

        # Values returned to the view function
        self.view_results = {
            'is_id': self.is_id,
            'not_found': self.beer_not_found,
            'no_similar_beers': self.similar_beers_not_found,
            'page': self.page,
            'search_term': self.search_term,
        }

    def get_beer(self):
        """Returns a dictionary of beer attributes or a not found response"""
        beer = lookup_beer(self.search_term, self.is_id)

        if isinstance(beer, int) and beer == 0:
            return self.brewery_db.get_beer(self.search_term, self.is_id)
        elif len(beer) == 1:
            return beer[0]
        else:
            return self.beer_not_found

    def get_style_id(self, beer):
        """Returns the beer style id if present or None"""
        if 'styleid' in beer and beer['styleid'] is not None:
            style_id = int(beer['styleid'])
            self.view_results['style_id'] = style_id
            return style_id
        elif 'styleId' in beer and beer['styleId'] is not None:
            style_id = int(beer['styleId'])
            self.view_results['style_id'] = style_id
            return style_id
        else:
            return None

    def get_abv_range(self, beer):
        """Returns the beer abv range if present or None"""
        if 'abv' in beer and beer['abv'] is not None:
            start_abv = int(float(beer['abv']))
        else:
            start_abv = None

        end_abv = start_abv + 1 if start_abv is not None else None
        abv_range = str(start_abv) + ',' + str(end_abv) if start_abv is not \
            None else None

        self.view_results['abv_range'] = abv_range
        return abv_range

    def get_params(self, beer):
        """Returns the BreweryDB API request params"""
        params = {
            'withBreweries': 'Y',
            'p': self.page
        }
        style_id = self.get_style_id(beer)
        abv_range = self.get_abv_range(beer)

        if style_id is not None:
            params['styleId'] = style_id
        else:
            return self.similar_beers_not_found

        if abv_range is not None:
            params['abv'] = abv_range

        return params

    def get_similar_beers(self, beer):
        """Returns a request response dictionary of similar beers"""
        params = self.get_params(beer)

        if params == self.similar_beers_not_found:
            self.view_results['beers'] = params
            return self.view_results

        api_results = self.brewery_db.\
            call_api(self.name_endpoint, params)

        self.view_results['number_of_pages'] = api_results['numberOfPages'] \
            if 'numberOfPages' in api_results else 0
        self.view_results['beers'] = api_results['data'] \
            if 'data' in api_results else api_results

        return self.view_results

    def search(self):
        """Creates an API request to the BreweryDB search endpoint, adds the
        response to the view results and returns the view results.
        """
        params = {'q': self.search_term, 'type': 'beer'}
        api_results = self.brewery_db.call_api(self.search_endpoint, params)

        self.view_results['number_of_pages'] = api_results['numberOfPages'] \
            if 'numberOfPages' in api_results else 0
        self.view_results['beers'] = api_results['data'] \
            if 'data' in api_results else api_results

        return self.view_results

    def get_results(self):
        """Returns a list of similar beers provided a valid input, else returns
        a not found response.
        """
        beer = self.get_beer()
        if beer == self.beer_not_found:
            return self.search()
        else:
            return self.get_similar_beers(beer)
