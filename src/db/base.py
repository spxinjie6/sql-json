from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy(session_options={'autocommit': True})


class GenColumn(db.Column):

    def __init__(self, *args, **kwargs):
        """SQLAlchemy 默认如果不指定 nullable 默认是 True.

        Source Code:
            self.primary_key = kwargs.pop('primary_key', False)
            self.nullable = kwargs.pop('nullable', not self.primary_key)

        修改规则为，如果不指定 nullable 那么默认值是 False.
        """
        if "nullable" not in kwargs:
            kwargs["nullable"] = False
        super(GenColumn, self).__init__(*args, **kwargs)


class HasIdMixin:
    id = db.Column('id', db.Integer, primary_key=True)


class HasCreateTimeAndLastUpdateTimeMixin:
    create_time = GenColumn('create_time', db.DateTime,
                            server_default=db.func.now())
    last_update_time = GenColumn('last_update_time', db.DateTime,
                                 server_default=db.func.now())


class TableMixin(HasIdMixin, HasCreateTimeAndLastUpdateTimeMixin):

    def __init__(self, **kwargs):
        self.create_time = kwargs.pop("create_time", datetime.now())
        self.last_update_time = kwargs.pop("last_update_time", datetime.now())

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
