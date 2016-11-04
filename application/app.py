from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_alchemydumps import AlchemyDumps, AlchemyDumpsCommand
from .settings import base


import logging

app = Flask(__name__)
app.config.from_object(base)

DEVELOPMENT=True
DEBUG=False

logger = logging.getLogger('app')


db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# init Alchemy Dumps
# manage.py alchemydumps create
# manage.py alchemydumps restore -d <id>
alchemydumps = AlchemyDumps(app, db)
manager.add_command('alchemydumps', AlchemyDumpsCommand)
