from brewmaster.database.schemas import schemas
from brewmaster.helpers import create_kwargs, for_each
from app import mysql


def save_beer(beer):
    fields = schemas["beer"].fields
    kwargs = for_each(fields, create_kwargs, beer, {})
    keys = tuple(key for key in kwargs.keys())
    values = tuple(value for value in kwargs.values())

    query = """
            INSERT INTO `beers` (%s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s);
            """
    args = keys + values

    return mysql.query(query, args)
