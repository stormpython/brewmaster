from pymysql import escape_string
from app import mysql


def lookup_beer(search_term, is_id):
    """Queries the MySQL database for a specific beer by name or id"""
    attr = 'id' if is_id is True else 'name'
    query = """
            SELECT `id`, `name`, `styleid`, `abv`
            FROM `beers`
            WHERE `%s` = '%s'
            """ % (attr, escape_string(search_term))

    return mysql.query(query)
