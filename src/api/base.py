# -*- coding: utf-8 -*-

import flask
import traceback
import flask_restful
import flask_restful.reqparse
import functools
import jsonschema
import werkzeug.exceptions
from flask import jsonify
from oslo_log import log as logging
from line_profiler import LineProfiler

from src.Exceptions import (
    BaseExceptions,
    ParameterErrorSystemException)

LOG = logging.getLogger(__name__)


def func_line_time(f):
    @functools.wraps(f)
    def decorator(*args, **kwargs):
        func_return = f(*args, **kwargs)
        lp = LineProfiler()
        lp_wrap = lp(f)
        lp_wrap(*args, **kwargs)
        lp.print_stats()
        return func_return
    return decorator


def _make_result(retcode: int, resp: dict = None, error: str = None):
    response = {
        "retcode": retcode,
        "request": flask_restful.request.path}
    if retcode == 0:
        response["resp"] = resp if resp else {}
    else:
        response["error"] = error
    return jsonify(response)


def catch_exceptions(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if not isinstance(e, BaseExceptions):
                LOG.error(traceback.format_exc())
                return _make_result(
                    retcode=1001,
                    error=repr(e))

            LOG.error("code: {}, message: {}".format(e.code, e.message))
            return _make_result(
                retcode=e.code,
                error=e.message)

    return wrapper


class ApiResource(flask_restful.Resource):

    method_decorators = [catch_exceptions]

    def __init__(self, *args, **kwargs):
        self.log = LOG
        self.parser_args = []
        self.parser = flask_restful.reqparse.RequestParser()
        super(ApiResource, self).__init__(*args, **kwargs)

    @staticmethod
    def make_ok(data: dict = None) -> dict:
        return _make_result(retcode=0,
                            resp=data)

    def parse_args(self):
        try:
            args = self.parser.parse_args()
        except werkzeug.exceptions.BadRequest as e:
            raise ParameterErrorSystemException(
                message="参数解析失败:[{}]".format(e.data["message"]))
        else:
            return args

    @staticmethod
    def get_json():
        return flask.request.get_json(force=True)

    def parse_json(self, schema):
        body = self.get_json()
        try:
            jsonschema.validate(body, schema)
        except Exception as e:
            raise ParameterErrorSystemException(
                message="JSON 格式验证失败:[{}]".format(str(e)))
        else:
            return body

    def add_argument(self, name, **kwargs):
        self.parser_args.append(name)
        self.parser.add_argument(name, **kwargs)
