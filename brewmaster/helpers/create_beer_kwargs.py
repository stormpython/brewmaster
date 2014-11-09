from . import for_each, create_kwarg


def create_beer_kwargs(beer):
    kwargs = {}
    fields = [
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

    for_each(fields, create_kwarg, beer, kwargs)
    return kwargs
