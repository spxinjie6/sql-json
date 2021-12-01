from oslo_log import log as logging

LOG = logging.getLogger(__name__)


class BaseExceptions(Exception):
    """ 异常基类  """

    def __init__(self, **kwargs):
        self.message = kwargs.get("message")
        LOG.error(self.message)
        super().__init__(self.message)


""" 系统级别错误 """


class ParameterErrorSystemException(BaseExceptions):
    """ 参数错误 """

    def __init__(self, *args, **kwargs):
        self.code = kwargs.get("code", 1004)
        super().__init__(*args, **kwargs)
