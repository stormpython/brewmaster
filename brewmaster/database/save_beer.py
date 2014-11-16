from brewmaster.database.schemas import schemas
from brewmaster.helpers import create_kwargs, for_each
from app import mysql


def save_beer(beer):
    fields = schemas['beer'].fields
    kwargs = {}

    # Create kwargs
    for_each(fields, create_kwargs, beer, kwargs)

    query = """
            INSERT INTO `beers` (id, name, description, abv, ibu,
                glasswareId, glass, styleId, style, isOrganic,
                foodPairings, originalGravity, labels,
                servingTemperature, servingTemperatureDisplay, status,
                statusDisplay, availableId, available, beerVariationId,
                beerVariation, year, createDate, updateDate)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s);
            """
    args = tuple(kwargs[key] for key in fields)

    return mysql.query(query, args)
