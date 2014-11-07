# Main Algorithm for Brew Master
#
# INPUT
# 1. Accepts a search term as input, which is either a beer or brand name.
#
# GET BEER AND IT'S ATTRIBUTES
# 2. The search term is looked up in the beer database.
# 3. If the beer is found in the database, a dict of beer attributes is
#    returned.
# 4. Else, an API call is made to the BreweryDB API beer endpoint.
# 5. If the beer is found in the API database, the beer is saved in the beer
#    database, and a dict of beer attributes is returned.
# ***IT'S IMPORTANT TO NOTE THAT ONLY 1 BEER SHOULD BE RETURNED HERE***
#
# GET LIST OF SIMILAR BEERS
# 6. If a beer is found above, the style_id and abv attributes are extracted
#    from the dictionary of beer attributes.
# 7. An API call is made to the beers endpoint with the style_id and abv
#    attributes as parameters to obtain a list of similar beers, which get
#    returned to the user.
#
# SEARCH FOR BEER NAME OR BRAND NAME
# 8. If a beer is not found in the first steps above, an API call is made to
#    the BreweryDB API search endpoint.
# 9. If there are any hits for the search term, a list of beers is returned.
#
# NO BEER OR BRAND NAME FOUND
# 10. If still no beer(s) are found, then the user receives a `Beer not found`
#    message.

from brew_master import BrewMaster

