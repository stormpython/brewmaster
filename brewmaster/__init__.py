"""
Algorithm for brewmaster

1. Accepts a beer name as input.
2. The beer name is used to query the beers database.

**If the beer is already stored in the database**
    3. The beer id is used to query the similar_beers database.
    4. The list of similar beers are returned to the user in order of similarity based on rank.

**If beer is not in database**
    5. An api call is made to obtain the relevant information for the beer.
    6. The results of the api call are saved in the beers database.
    7. The characteristics of the beer are then used to obtain a list of beers with similar characteristics
        through another api call.
    8. The beer name the user entered + its characteristics and the list of similar beers + their characteristics
        returned from the api call are run through the algorithm to determine the rank order.
    9. The list of similar beers, characteristics, and rank are all saved in the similar_beers database.
    10. The results of the algorithm are returned to the user in rank order.
"""