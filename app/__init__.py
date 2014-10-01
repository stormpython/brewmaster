from flask import Flask
from config import config
from mysql import MySQL
import os


# Creates our application.
app = Flask(__name__)
config_name = os.getenv('FLASK_CONFIG') or 'default'
app.config.from_object(config[config_name])
config[config_name].init_app(app)

mysql = MySQL(app)


from app import views, errors
