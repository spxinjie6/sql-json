from oslo_config import cfg
CONF = cfg.CONF

# 默认配置
DEFAULT_OPTS = [
    cfg.BoolOpt("debug"),
    cfg.StrOpt("log_dir"),
    cfg.StrOpt("env")
]
CONF.register_opts(DEFAULT_OPTS, "DEFAULT")
default_conf = CONF.DEFAULT

# gunicorn 配置
GUNICORN_OPTS = [
    cfg.StrOpt("bind"),
    cfg.IntOpt("workers"),
    cfg.StrOpt("worker_class")
]
CONF.register_opts(GUNICORN_OPTS, "GUNICORN")
gunicorn_conf = CONF.GUNICORN

# MySQL 配置
MYSQL_OPTS = [
    cfg.StrOpt("host"),
    cfg.IntOpt("port"),
    cfg.StrOpt("username"),
    cfg.StrOpt("password"),
    cfg.StrOpt("database"),
    cfg.StrOpt("charset")
]
CONF.register_opts(MYSQL_OPTS, "MYSQL")
mysql_conf = CONF.MYSQL
