import flask
import logging
import os
basedir=os.path.abspath(os.path.dirname(__file__)+'/../')
LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
             'simple': {
                  'format': '%(levelname)s: %(message)s'
        },
        },
        'handlers': {
            'file':{
                  'class' : 'logging.handlers.RotatingFileHandler',
                  'formatter': 'simple',
                  'filename': basedir+'/log/logconfig.log',
                  'level': 'INFO',
                  'maxBytes': 1024,
                  'backupCount': 3
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
