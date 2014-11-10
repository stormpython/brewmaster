from app import app
from api import API
from database import lookup_beer, save_beer


class BrewMaster:

    def __init__(self, search_term, is_id=False, page=1):
        self.search_term = search_term
        self.is_id = is_id
        self.page = page

        # API settings
        self.api_url = app.config["BREWERY_DB_API_URL"]
        self.api_key = app.config["BREWERY_DB_API_KEY"]
        self.brewery_db_api = API(self.api_url, self.api_key)
        self.name_endpoint = "beers"
        self.id_endpoint = "beer/" + self.search_term if self.is_id is True \
            else None
        self.search_endpoint = "search"

        # Not found response
        self.beer_not_found = app.config["NO_BEER_FOUND"]
        self.similar_beers_not_found = app.config["SIMILAR_BEERS_NOT_FOUND"]

    def call_api(self, endpoint, params):
        results = self.brewery_db_api.get(endpoint, params).json()

        if "data" in results:
            return results["data"]
        else:
            return self.beer_not_found

    def call_beer_api_endpoint(self):
        params = {}

        if self.is_id is True:
            endpoint = self.id_endpoint
        else:
            endpoint = self.name_endpoint
            params["name"] = self.search_term

        results = self.call_api(endpoint, params)

        if isinstance(results, str):
            return results
        elif len(results) == 1 or isinstance(results, dict):
            beer = results[0] if len(results) == 1 else results
            save_beer(beer)
            return beer
        else:
            return self.beer_not_found

    def get_beer(self):
        beer = lookup_beer(self.search_term, self.is_id)

        if isinstance(beer, int) and beer == 0:
            return self.call_beer_api_endpoint()
        elif len(beer) == 1:
            return beer[0]
        else:
            return self.beer_not_found

    def get_similar_beers(self, beer):
        params = {
            "withBreweries": "Y",
            "p": self.page
        }

        if "styleid" in beer and beer["styleid"] is not None:
            style_id = int(beer["styleid"])
        elif "styleId" in beer and beer["styleId"] is not None:
            style_id = int(beer["styleId"])
        else:
            style_id = None

        if "abv" in beer and beer["abv"] is not None:
            start_abv = int(float(beer["abv"]))
        else:
            start_abv = None

        end_abv = start_abv + 1 if start_abv is not None else None
        abv_range = str(start_abv) + "," + str(end_abv) if start_abv is not \
            None else None

        if style_id is not None and abv_range is not None:
            params["styleId"] = style_id
            params["abv"] = abv_range
        elif style_id is not None:
            params["styleId"] = style_id
        else:
            return "No similar beers found"

        beers = self.call_api(self.name_endpoint, params)

        return {
            "search_term": self.search_term,
            "is_id": self.is_id,
            "style_id": style_id,
            "abv_range": abv_range,
            "not_found": self.beer_not_found,
            "page": self.page,
            "beers": beers
        }

    def search(self):
        params = {"q": self.search_term, "type": "beer"}
        beers = self.call_api(self.search_endpoint, params)

        return {
            "search_term": self.search_term,
            "is_id": self.is_id,
            "not_found": self.beer_not_found,
            "page": self.page,
            "beers": beers
        }

    def get_results(self):
        beer = self.get_beer()
        if beer == self.beer_not_found:
            return self.search()
        else:
            return self.get_similar_beers(beer)
