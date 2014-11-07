from app import app, mysql
from api import API
from .helpers import for_each, create_kwarg
from pymysql import escape_string


class BrewMaster:
    api_call_count = 0

    def __init__(self, search_term):
        self.search_term = search_term
        self.db_table = "beer"
        self.not_found_response = app.config["NOT_FOUND_RESPONSE"]
        self.api_url = app.config["BREWERY_DB_API_URL"]
        self.api_key = app.config["BREWERY_DB_API_KEY"]
        self.brewery_db_api = API(self.api_url, self.api_key)
        self.beer_endpoint = "beers"
        self.search_endpoint = "search"
        self.api_call_limit = app.config["BREWERY_DB_API_LIMIT"]
        self.api_call_limit_message = app.config["API_LIMIT_REACHED_MESSAGE"]

    def db_lookup_search_term(self):
        """Returns an array/list of dictionaries or 0.

        Queries the MySQL beer table for the beer in the `search_term`.
        Note: 0 == not in database
        """
        query = """SELECT id, name, style_id, abv FROM beer WHERE name = %s"""
        args = (escape_string(self.search_term))
        return mysql.query(query, args)

    @staticmethod
    def get_beer_kwargs(beer):
        kwargs = {}
        attrs = [
            "id",
            "name",
            "description",
            "abv",
            "ibu",
            "glassware_id",
            "style_id",
            "is_organic",
            "food_pairings",
            "original_gravity",
            "labels_icon",
            "labels_medium",
            "labels_large",
            "serving_temperature",
            "serving_temperature_display",
            "status",
            "status_display",
            "available_id",
            "beer_variation_id",
            "year",
            "create_date",
            "update_date"
        ]

        for_each(attrs, create_kwarg, beer, kwargs)
        return kwargs

    def db_save_beer(self, beer):
        kwargs = self.get_beer_kwargs(beer)
        query = """
                INSERT INTO beer (id, name, description, abv, ibu,
                    glassware_id, style_id, is_organic, food_pairings,
                    original_gravity, labels_icon, labels_medium, labels_large,
                    serving_temperature, serving_temperature_display, status,
                    status_display, available_id, beer_variation_id, year,
                    create_date, update_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s);
                """
        args = tuple(kwargs[attr] for attr in kwargs)

        mysql.query(query, args)

    def call_api(self, endpoint, params):
        """Returns an array/list of dictionaries, a not found string, or an
        api limit string.

        Accepts a endpoint string and a dictionary of parameters.

        Makes an api call to the specified endpoint with the specified
        parameters.
        """
        if self.api_call_count < self.api_call_limit:
            results = self.brewery_db_api.get(endpoint, params).json()

            if 'data' in results:
                return results['data']
            else:
                return self.not_found_response
        else:
            return self.api_call_limit_message

    def call_beer_api_endpoint(self):
        """Returns a JSON response for 1 beer, a not found string, or an api
        limit string.

        This function should only return a dictionary for 1 beer.

        If the API request limit has not been reached, an API call is made
        to the BreweryDB `beers` endpoint using the `search_term`. If no
        beer is found, a not found message is returned.
        """
        params = {"name": self.search_term}
        result = self.call_api(self.beer_endpoint, params)

        if isinstance(result, str):
            return result
        elif len(result) == 1:
            return result[0]
        else:
            return self.not_found_response

    def get_beer(self):
        """Returns a dictionary, JSON response, or a not found string.

        Queries the database using the `search_term` for a specific beer.
        If the beer is not found, an API call is made. If a beer is still
        not found, a not found response is returned.
        """
        beer = self.db_lookup_search_term()

        if isinstance(beer, int) and beer == 0:
            return self.call_beer_api_endpoint()
        elif len(beer) == 1:
            return beer[0]
        else:
            return self.not_found_response

    def get_similar_beers(self, beer):
        """Returns an array/list, an api limit string, or a not found string.

        Accepts a dictionary of beer attributes as input.

        Makes an API call to the BreweryDB `beers` endpoint using the
        `styleId` and `abv` attributes. The `styleId` attribute is
        required.
        """
        style_id = int(beer["styleId"]) if 'styleId' in beer else None
        start_abv = int(float(beer["abv"])) if 'abv' in beer else None
        end_abv = start_abv + 1 if start_abv is not None else None
        abv_range = str(start_abv) + "," + str(end_abv) \
            if start_abv is not None else None

        if style_id is not None and abv_range is not None:
            params = {"styleId": style_id, "abv": abv_range}
        elif style_id is not None:
            params = {"styleId": style_id}
        else:
            return self.not_found_response

        return self.call_api(self.beer_endpoint, params)

    def search(self):
        """Makes an API call to the BreweryDB search endpoint based on the
        search_term. Returns a list of beers, else returns a not found response
        """
        params = {"q": self.search_term}
        return self.call_api(self.search_endpoint, params)

    def get_results(self):
        """Main algorithm for the BrewMaster class. It queries for a specific
        beer based on the `search_term` provided and returns a listing of
        beers or a not found response
        """
        beer = self.get_beer()
        if beer == self.not_found_response:
            return self.search()
        else:
            return self.get_similar_beers(beer)

