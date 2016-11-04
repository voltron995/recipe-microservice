from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_alchemydumps import AlchemyDumps, AlchemyDumpsCommand
from .settings import base

from config.logconf import LOGGING
import logging.config

app = Flask(__name__)
app.config.from_object(base)
<<<<<<< HEAD
DEVELOPMENT=True
DEBUG=False

logger = logging.getLogger('app')
=======

>>>>>>> 9f9c7a847d4817afb144a0849195483adeca29de
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# init Alchemy Dumps
# manage.py alchemydumps create
# manage.py alchemydumps restore -d <id>
alchemydumps = AlchemyDumps(app, db)
manager.add_command('alchemydumps', AlchemyDumpsCommand)
