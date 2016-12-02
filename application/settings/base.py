import os
from .locals import DB_SETTINGS
import logging
import logging.config
APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
DEBUG = True

SQLALCHEMY_DATABASE_URI = "{rdbms}://{user}:{password}@{host}:{port}/{db_name}".format(**DB_SETTINGS)
SQLALCHEMY_TRACK_MODIFICATIONS = False
basedir=os.path.abspath(os.path.dirname(__file__)+'/../../')

LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
             'simple': {
                  'format': "%(asctime)s %(name)-15s %(levelname)-8s %(message)s"
        },
        },
        'handlers': {
            'file':{
                  'class' : 'logging.handlers.RotatingFileHandler',
                  'formatter': 'simple',
                  'filename': basedir+'/log/logconfig.log',
                  'level': 'INFO'
                  },

            'console': {
                  'class': 'logging.StreamHandler',
                  'level': 'DEBUG',
                  'formatter': 'simple',
                  'stream': 'ext://sys.stdout'
              }
          },
          'loggers': {
              'app': {
                  'handlers': ['file', 'console'],
                  'level': 'INFO'
              }
          }
      }
logging.config.dictConfig(LOGGING)
