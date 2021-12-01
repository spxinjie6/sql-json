import os
import sys
import multiprocessing
from abc import ABC

import gunicorn.app.base
from oslo_config import cfg
from oslo_log import log as logging

from src.libs.config import gunicorn_conf, default_conf
from src.app import make_app

LOG = logging.getLogger(__name__)
CONF = cfg.CONF
logging.register_options(CONF)


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


class StandaloneApplication(gunicorn.app.base.BaseApplication, ABC):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def app():
    CONF(sys.argv[1:])
    if not os.path.exists(CONF.DEFAULT.log_dir):
        os.makedirs(CONF.DEFAULT.log_dir)
    logging.setup(CONF, "python-template-api")
    LOG.info("启动 Python 模板工程...")
    if default_conf.get("env") == "dev":
        host, port = gunicorn_conf.get("bind").split(":")

        make_app().run(host=host,
                       port=int(port),
                       debug=default_conf.get("debug"))
    else:
        StandaloneApplication(
            make_app(),
            gunicorn_conf).run()
