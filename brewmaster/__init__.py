"""
Algorithm for brewmaster

1. User inputs beer name into search box and clicks search.
2. The beer name is used to query the beers database.

**If the beer and its list of similar beers is already stored in the database**
    3. If the beer is in the database, the beer id is used to query the similar_beers database.
    4. The list of similar beers are returned to the user in order of similarity based on rank.

**If data is not in database**
    5. Else, an api call is made to obtain the relevant information for the beer.
    6. The results of the api call are saved in the beers database.
    7. The characteristics of the beer are then used to obtain a list of beers with similar characteristics
        thru another api call.
    8. The beer name + its characteristics the user entered and the list of similar beers + their characteristics
        returned from the api call are run through the algorithm to determine the rank order.
    9. The list of similar beers, characteristics, and rank are all saved in the similar_beers database.
    10. The results of the algorithm are returned to the user in rank order.
"""