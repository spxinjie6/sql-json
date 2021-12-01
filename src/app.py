import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask import (
    Flask,
    abort)
from flask_docs import ApiDoc
from werkzeug.routing import BaseConverter
from oslo_log import log as logging

from src import (
    db,
    api)


LOG = logging.getLogger(__name__)


class RegexConverter(BaseConverter):
    """ 使 Flask 路由支持正则 """
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


def make_app():
    app = Flask(__name__)
    app.config['API_DOC_MEMBER'] = ['api', 'platform']
    app.config['RESTFUL_API_DOC_EXCLUDE'] = []
    ApiDoc(app)
    app.url_map.converters['regex'] = RegexConverter
    LOG.info("加载 DB 插件...")
    db.init(app)
    LOG.info("加载 API 插件...")
    api.init(app)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        return abort(404)

    return app
