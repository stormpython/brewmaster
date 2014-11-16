import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Flask application key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    # MySQL shared connection settings
    MYSQL_DATABASE_HOST = 'localhost'
    MYSQL_DATABASE_PORT = 3306
    MYSQL_DATABASE_USER = os.environ.get('MYSQL_DATABASE_USER') or None
    MYSQL_DATABASE_PASSWORD = os.environ.get('MYSQL_DATABASE_PASSWORD') or None
    MYSQL_DATABASE_DB = None
    MYSQL_DATABASE_CHARSET = 'utf8'

    # BreweryDB API info
    # For more information, see: http://www.brewerydb.com/developers/docs
    BREWERY_DB_API_URL = 'http://api.brewerydb.com/v2'
    BREWERY_DB_API_KEY = os.environ.get('BREWERY_DB_API_KEY')

    # BrewMaster Responses
    NO_BEER_FOUND = 'The beer or brand name you entered was not found.'
    SIMILAR_BEERS_NOT_FOUND = 'There were no similar beers found'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
