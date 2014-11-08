from app import app, mysql
from api import API
from .helpers import for_each, create_kwarg
from pymysql import escape_string
import json


class BrewMaster:

    def __init__(self, search_term):
        self.search_term = search_term
        self.db_table = "beers"
        self.api_url = app.config["BREWERY_DB_API_URL"]
        self.api_key = app.config["BREWERY_DB_API_KEY"]
        self.brewery_db_api = API(self.api_url, self.api_key)
        self.beer_endpoint = "beers"
        self.search_endpoint = "search"
        self.not_found_response = app.config["NOT_FOUND_RESPONSE"]

    def db_lookup_search_term(self):
        """Returns an array/list of dictionaries or 0.

        Queries the MySQL beer table for the beer in the `search_term`.
        Note: 0 means not in database
        """
        query = """SELECT id, name, styleid, abv FROM beers WHERE name = %s"""
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
            "glasswareId",
            "glass",
            "styleId",
            "style",
            "isOrganic",
            "foodPairings",
            "originalGravity",
            "labels",
            "servingTemperature",
            "servingTemperatureDisplay",
            "status",
            "statusDisplay",
            "availableId",
            "available",
            "beerVariationId",
            "beerVariation",
            "year",
            "createDate",
            "updateDate"
        ]

        for_each(attrs, create_kwarg, beer, kwargs)
        return kwargs

    def db_save_beer(self, beer):
        kwargs = self.get_beer_kwargs(beer)

        query = """
                INSERT INTO beers (id, name, description, abv, ibu,
                    glasswareId, glass, styleId, style, isOrganic,
                    foodPairings, originalGravity, labels, servingTemperature,
                    servingTemperatureDisplay, status, statusDisplay,
                    availableId, available, beerVariationId, beerVariation,
                    year, createDate, updateDate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s);
                """
        args = (
            kwargs["id"],
            escape_string(kwargs["name"]),
            escape_string(kwargs["description"]),
            kwargs["abv"],
            kwargs["ibu"],
            kwargs["glasswareId"],
            json.dumps(kwargs["glass"]) if kwargs["glass"] is not None else None,
            kwargs["styleId"],
            json.dumps(kwargs["style"]) if kwargs["style"] is not None else None,
            kwargs["isOrganic"],
            kwargs["foodPairings"],
            kwargs["originalGravity"],
            json.dumps(kwargs["labels"]) if kwargs["labels"] is not None else None,
            kwargs["servingTemperature"],
            kwargs["servingTemperatureDisplay"],
            kwargs["status"],
            kwargs["statusDisplay"],
            kwargs["availableId"],
            json.dumps(kwargs["available"]) if kwargs["available"] is not None else None,
            kwargs["beerVariationId"],
            json.dumps(kwargs["beerVariation"]) if kwargs["beerVariation"] is not None else None,
            kwargs["year"],
            kwargs["createDate"],
            kwargs["updateDate"]
        )

        response = mysql.query(query, args)
        print response

    def call_api(self, endpoint, params):
        """Returns an array/list of dictionaries, a not found string, or an
        api limit string.

        Accepts a endpoint string and a dictionary of parameters.

        Makes an api call to the specified endpoint with the specified
        parameters.
        """
        results = self.brewery_db_api.get(endpoint, params).json()

        if "data" in results:
            return results["data"]
        else:
            return self.not_found_response

    def call_beer_api_endpoint(self):
        """Returns a JSON response for 1 beer, a not found string, or an api
        limit string.

        This function should only return a dictionary for 1 beer.

        If the API request limit has not been reached, an API call is made
        to the BreweryDB `beers` endpoint using the `search_term`. If no
        beer is found, a not found message is returned.
        """
        params = {"name": self.search_term}
        results = self.call_api(self.beer_endpoint, params)

        if isinstance(results, str):
            return results
        elif len(results) == 1:
            beer = results[0]
            self.db_save_beer(beer)
            return beer
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
        if "styleid" in beer:
            style_id = int(beer["styleid"])
        elif "styleId" in beer:
            style_id = int(beer["styleId"])
        else:
            style_id = None

        start_abv = int(float(beer["abv"])) if "abv" in beer else None
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
        """Returns a JSON response or a not found string.

        Makes an API call to the BreweryDB search endpoint based on the
        search_term.
        """
        params = {"q": self.search_term, "type": "beer"}
        return self.call_api(self.search_endpoint, params)

    def get_results(self):
        """Returns a JSON response or a not found string.

        Main algorithm for the BrewMaster class. It queries for a specific
        beer based on the `search_term` provided and returns a listing of
        beers or a not found response.
        """
        beer = self.get_beer()
        if beer == self.not_found_response:
            return self.search()
        else:
            return self.get_similar_beers(beer)
