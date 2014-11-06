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
        self.api_call_limit = app.config["BREWERY_DB_API_LIMIT"]
        self.api_call_limit_message = app.config["API_LIMIT_REACHED_MESSAGE"]

    def db_lookup_search_term(self):
        """Queries database for a specific beer by name, returns MySQL class
         response"""
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

    def call_beers_api_endpoint(self):
        """Queries the BreweryDB beers endpoint for a specific beer. If the
         beer is found, it saves the beer to the database and returns that
         beer else returns not found response"""
        endpoint = "beers"
        params = {
            "name": self.search_term
        }

        if self.api_call_count < self.api_call_limit:
            # Call API and save response
            api_results = self.brewery_db_api.get(endpoint, params).json()

            if 'totalResults' in api_results and api_results['totalResults'] == 1:
                # If there is one beer in the api_results,
                # return that beer object
                beer = api_results['data'][0]

                # Save beer to database
                self.db_save_beer(beer)
                return beer
            else:
                return self.not_found_response
        else:
            return self.api_call_limit_message

    def get_beer(self):
        """Does a look up for a specific beer and returns that beer if present,
        else returns not found response"""

        # Look up beer in database
        beer = self.db_lookup_search_term()

        if isinstance(beer, int) and beer == 0:
            # if beer is not in the database:
            # Make an API call
            return self.call_beers_api_endpoint()
        elif len(beer) == 1:
            # if 1 beer is in the database response
            # Return the result from the database
            return beer[0]
        else:
            # if response from database has more than 1 beer, return a not
            #  found response. get_beer() should only return 1 beer
            return self.not_found_response

    def get_similar_beers(self, beer):
        """Makes an API call to the BreweryDB beers endpoint based on the
        `styleId` and `abv` if present. Returns a list of beers that match
        the `styleId` and `abv`, else returns a not found response"""
        endpoint = "beers"
        style_id = int(beer["styleId"]) if 'styleId' in beer else None

        # Calculate the abv range
        start_abv = int(float(beer["abv"])) if 'abv' in beer else None
        end_abv = start_abv + 1 if start_abv is not None else None
        abv_range = str(start_abv) + "," + str(end_abv) \
            if start_abv is not None else None

        # Only make an API call if `styleId` is present
        if style_id is not None and abv_range is not None:
            params = {"styleId": style_id, "abv": abv_range}
        elif style_id is not None:
            params = {"styleId": style_id}
        else:
            return self.not_found_response

        if self.api_call_count < self.api_call_limit:
            # Call API and save the results
            results = self.brewery_db_api.get(endpoint, params).json()
            if 'totalResults' in results and results['totalResults'] > 1:
                # if results, return the data array
                return results.json()['data']
            else:
                return self.not_found_response
        else:
            return self.api_call_limit_message

    def search(self):
        """Makes an API call to the BreweryDB search endpoint based on the
        search_term. Returns a list of beers, else returns a not found
         response"""
        endpoint = "search"
        params = {"q": self.search_term}

        # Call API and save results
        results = self.brewery_db_api.get(endpoint, params).json()
        if 'data' in results:
            # if data array present in results, return data array
            return results['data']
        else:
            return self.not_found_response

    def get_results(self):
        """Main algorithm for the BrewMaster class. It queries for a specific
        beer based on the `search_term` provided and returns a listing of
        beers or a not found response"""

        # Query for beer in database or API
        beer = self.get_beer()

        if beer == self.not_found_response:
            # if no beer found, query for beer using the API search endpoint
            return self.search()
        else:
            # if beer found, get list of similar beers
            return self.get_similar_beers(beer)

