from flask_sqlalchemy import SQLAlchemy

from src.libs.config import (
    default_conf,
    mysql_conf)


def init(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://{username}:{password}"\
        "@{host}/{database}".format(
            username=mysql_conf.get("username"),
            password=mysql_conf.get("password"),
            host="{}:{}".format(mysql_conf.get("host"),
                                mysql_conf.get("port")),
            database=mysql_conf.get("database"))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    if default_conf.get("debug"):
        app.config['SQLALCHEMY_ECHO'] = True
    db = SQLAlchemy(app)
    db.init_app(app)
