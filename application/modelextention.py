import datetime
import re
from .app import db


class DateMixin(object):
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

def slugify(s):
    return re.sub('[^\w]+', '-', s).lower()

def create_table(table1, table2, arg=None):
    table = db.Table(table1 + '_' + table2,
        db.Column(table1+'_id', db.Integer, db.ForeignKey(table1+'.id')),
        db.Column(table2+'_id', db.Integer, db.ForeignKey(table2+'.id')))
    if arg:
        table.append_column(db.Column(arg, db.Integer))
    return table

class ManyToManyClass:
    pass