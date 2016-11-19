import datetime
import re
from .app import db


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
    @classmethod
    def get_attributes(cls):
        attrs = cls.__mapper__.columns.keys()
        attrs.extend(cls.__mapper__.relationships.keys())
        attributes = [attr for attr in attrs 
                            if not attr.endswith('_id') and 
                                not attr.endswith('_backref')]
        return attributes


class DateMixin():
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow, 
                                            onupdate=datetime.datetime.utcnow)


class BaseModel(DateMixin):
    id = db.Column(db.SmallInteger, primary_key=True)
    slug = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return '<{}} {}>'.format(self.__class__.__name__, self.name)

    @classmethod
    def get_attributes(cls):
        attrs = cls.__mapper__.columns.keys()
        attrs.extend(cls.__mapper__.relationships.keys())
        attributes = [attr for attr in attrs 
                    if not attr.endswith('_backref')]
        return attributes

