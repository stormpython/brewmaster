from app import app
from database import lookup_beer
from brewmaster.brewerydb_api import BreweryDBApi


class BrewMaster:

    def __init__(self, search_term, is_id=False, page=1):
        self.search_term = search_term
        self.is_id = is_id
        self.page = page

        # API settings
        self.brewery_db_api = BreweryDBApi()
        self.name_endpoint = "beers"
        self.search_endpoint = "search"

        # Not found response
        self.beer_not_found = app.config["NO_BEER_FOUND"]
        self.similar_beers_not_found = app.config["SIMILAR_BEERS_NOT_FOUND"]

        # Values returned to the view function
        self.view_results = {
            "is_id": self.is_id,
            "not_found": self.beer_not_found,
            "page": self.page,
            "search_term": self.search_term,
        }

    def get_beer(self):
        beer = lookup_beer(self.search_term, self.is_id)

        if isinstance(beer, int) and beer == 0:
            return self.brewery_db_api.call_beer_api_endpoint(
                self.search_term, self.is_id)
        elif len(beer) == 1:
            return beer[0]
        else:
            return self.beer_not_found

    def get_style_id(self, beer):
        if "styleid" in beer and beer["styleid"] is not None:
            style_id = int(beer["styleid"])
            self.view_results["style_id"] = style_id
            return style_id
        elif "styleId" in beer and beer["styleId"] is not None:
            style_id = int(beer["styleId"])
            self.view_results["style_id"] = style_id
            return style_id
        else:
            return None

    def get_abv_range(self, beer):
        if "abv" in beer and beer["abv"] is not None:
            start_abv = int(float(beer["abv"]))
        else:
            start_abv = None

        end_abv = start_abv + 1 if start_abv is not None else None
        abv_range = str(start_abv) + "," + str(end_abv) if start_abv is not \
            None else None

        self.view_results["abv_range"] = abv_range
        return abv_range

    def get_similar_beers(self, beer):
        params = {
            "withBreweries": "Y",
            "p": self.page
        }
        style_id = self.get_style_id(beer)
        abv_range = self.get_abv_range(beer)

        if style_id is not None:
            params["styleId"] = style_id
        else:
            return "No similar beers found"

        if abv_range is not None:
            params["abv"] = abv_range

        self.view_results["beers"] = self.brewery_db_api.\
            call_api(self.name_endpoint, params)
        return self.view_results

    def search(self):
        params = {"q": self.search_term, "type": "beer"}
        self.view_results["beers"] = self.brewery_db_api.\
            call_api(self.search_endpoint, params)
        return self.view_results

    def get_results(self):
        beer = self.get_beer()
        if beer == self.beer_not_found:
            return self.search()
        else:
            return self.get_similar_beers(beer)
