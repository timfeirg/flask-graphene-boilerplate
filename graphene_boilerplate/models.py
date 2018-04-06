import sqlalchemy.orm.exc
from datetime import datetime
from flask_sqlalchemy import sqlalchemy as sa
from sqlalchemy import inspect

from graphene_boilerplate.ext import db
from graphene_boilerplate.utils import logger


class BaseModelMixin(db.Model):

    __abstract__ = True

    # can't name this id, see
    # https://stackoverflow.com/questions/46490229/retrieve-the-object-id-in-graphql
    id_ = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created = db.Column(db.DateTime, server_default=sa.sql.func.now())
    updated = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    @classmethod
    def create(cls, **kwargs):
        b = cls(**kwargs)
        db.session.add(b)
        db.session.commit()
        return b

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_multi(cls, ids):
        return [cls.get(i) for i in ids]

    @classmethod
    def get_all(cls, start=0, limit=None):
        q = cls.query.order_by(cls.id.desc())
        if not any([start, limit]):
            return q.all()
        return q[start:start + limit]

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except sqlalchemy.orm.exc.ObjectDeletedError:
            db.session.rollback()
            logger.warn('Error during deleting: Object %s already deleted', self)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.id == other.id

    def __hash__(self):
        return hash((self.__class__, self.id))

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Item(BaseModelMixin):
    __tablename__ = 'item'
    key = db.Column(db.String(64), unique=True)
    value = db.Column(db.JSON)
