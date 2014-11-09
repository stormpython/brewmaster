from . import create_beer_kwargs
from pymysql import escape_string
from app import mysql
import json


def save_beer(beer):
    kwargs = create_beer_kwargs(beer)

    query = """
                INSERT INTO `beers` (id, name, description, abv, ibu,
                    glasswareId, glass, styleId, style, isOrganic,
                    foodPairings, originalGravity, labels,
                    servingTemperature, servingTemperatureDisplay,
                    status, statusDisplay, availableId, available,
                    beerVariationId, beerVariation, year, createDate,
                    updateDate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s, %s);
                """
    args = (
        kwargs["id"],
        escape_string(kwargs["name"]) if kwargs["name"] is not None else None,
        escape_string(kwargs["description"]) if kwargs["description"] is not None else None,
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

    return mysql.query(query, args)

