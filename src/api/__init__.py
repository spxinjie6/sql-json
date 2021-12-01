import flask_restful
from src.api.v1 import init as v1_init


def init(app):
    restful_api = flask_restful.Api(app)
    v1_init(restful_api)
