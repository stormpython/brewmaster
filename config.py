import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Flask application key
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"

    # MySQL shared connection settings
    MYSQL_DATABASE_PORT = 3306
    MYSQL_DATABASE_HOST = os.getenv("MYSQL_DATABASE_HOST") or "localhost"
    MYSQL_DATABASE_USER = os.getenv("MYSQL_DATABASE_USER") or None
    MYSQL_DATABASE_PASSWORD = os.getenv("MYSQL_DATABASE_PASSWORD") or None
    MYSQL_DATABASE_DB = os.getenv("MYSQL_DATABASE_DB") or None
    MYSQL_DATABASE_CHARSET = "utf8"

    # BreweryDB API info
    # For more information, see: http://www.brewerydb.com/developers/docs
    BREWERY_DB_API_URL = "http://api.brewerydb.com/v2"
    BREWERY_DB_API_KEY = os.environ.get("BREWERY_DB_API_KEY")
    BREWERY_DB_API_LIMIT = 400

    API_LIMIT_REACHED_MESSAGE = "We have reached our daily API request " \
                                "limit. We are sorry for the inconvenience. " \
                                "Please try again tomorrow."

    # BrewMaster Responses
    NOT_FOUND_RESPONSE = "The beer or brand name you entered was not found."

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,

    "default": DevelopmentConfig
}
