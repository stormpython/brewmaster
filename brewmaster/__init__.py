from brew_master import BrewMaster

# Main Algorithm for Brew Master
#
# 1. Accepts a search term, which is either a beer or brand, name as input.
# 2. The search term is looked up in the beers database.
# 3. If the beer is found in the database, returns a dict of beer attributes.
# 4. Else, makes an API call to the BreweryDB beers endpoint.
# 5. If the beer is found in the API database, returns a dict of beer
#    attributes.
# 6. Save beer into the database.
# 7. The style_id and abv beer attributes are extracted from the beer dict.
# 8. An API call is made to the beers endpoint with style_id and abv values to
#    obtain a list of similar beers. This list is returned as an list of dicts
#    for each beer.
# 9. If the search term is not found, an API call is made to the search
#    endpoint.
# 10. If results are returned, the list of dicts for each beer is returned.
# 11. Else, if no results are returned, "search term could not be found" is
#    returned.
