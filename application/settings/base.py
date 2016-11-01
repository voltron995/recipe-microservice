import os
from .secrets import DB_SETTINGS


class Configuration:
    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "{rdbms}://{user}:{password}@{host}:{port}/{db_name}".format(**DB_SETTINGS)
    SQLALCHEMY_TRACK_MODIFICATIONS = False