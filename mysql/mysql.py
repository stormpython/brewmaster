###############################################################################
# Python class that allows you to access MySQL directly from your
# Flask application. The code was taken from:
# https://github.com/cyberdelia/flask-mysql/blob/master/flaskext/mysql.py
# and modified to use PyMySQL: https://github.com/PyMySQL/PyMySQL
###############################################################################

from __future__ import absolute_import
from flask import _app_ctx_stack
import pymysql


class MySQL(object):
    """Allows you to access MySQL directly from you Flask application"""
    def __init__(self, app=None):
        if app is not None:
            self.app = app
            self.init_app(self.app)
        else:
            self.app = None

    def init_app(self, app):
        """Initializes the class with your Flask application"""
        self.app = app
        self.app.config.setdefault('MYSQL_DATABASE_HOST', 'localhost')
        self.app.config.setdefault('MYSQL_DATABASE_PORT', 3306)
        self.app.config.setdefault('MYSQL_DATABASE_USER', None)
        self.app.config.setdefault('MYSQL_DATABASE_PASSWORD', None)
        self.app.config.setdefault('MYSQL_DATABASE_DB', None)
        self.app.config.setdefault('MYSQL_DATABASE_CHARSET', 'utf8')
        self.app.teardown_request(self.teardown_request)
        self.app.before_request(self.before_request)

    def connect(self):
        """Creates a connection to the MySQL database"""
        kwargs = {}
        if self.app.config['MYSQL_DATABASE_HOST']:
            kwargs['host'] = self.app.config['MYSQL_DATABASE_HOST']
        if self.app.config['MYSQL_DATABASE_PORT']:
            kwargs['port'] = self.app.config['MYSQL_DATABASE_PORT']
        if self.app.config['MYSQL_DATABASE_USER']:
            kwargs['user'] = self.app.config['MYSQL_DATABASE_USER']
        if self.app.config['MYSQL_DATABASE_PASSWORD']:
            kwargs['passwd'] = self.app.config['MYSQL_DATABASE_PASSWORD']
        if self.app.config['MYSQL_DATABASE_DB']:
            kwargs['db'] = self.app.config['MYSQL_DATABASE_DB']
        if self.app.config['MYSQL_DATABASE_CHARSET']:
            kwargs['charset'] = self.app.config['MYSQL_DATABASE_CHARSET']
        kwargs['autocommit'] = True
        return pymysql.connect(**kwargs)

    def cursor(self):
        """Provides access to the MySQL database cursor"""
        conn = self.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        return cur

    def query(self, query, args=None):
        """An interface for submitting a query to the MySQL database"""
        cur = self.cursor()
        count = cur.execute(query, args)
        if count == 0:
            return count
        else:
            results = cur.fetchall()
            cur.close()
            return results

    def before_request(self):
        """Sets up database connection before an HTTP request"""
        ctx = _app_ctx_stack.top
        ctx.pymysql = self.connect()

    def teardown_request(self, exception):
        """Tears down the Mysql database connection"""
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'pymysql'):
            ctx.pymysql.close()

    def get_db(self):
        """Returns access to the database"""
        ctx = _app_ctx_stack.top
        if ctx is not None:
            return ctx.pymysql
