# -*- coding: utf-8 -*-

from src.db.base import (
    db,
    TableMixin,
    GenColumn)


class DemoObjectModel(db.Model, TableMixin):
    """demo_object
    CREATE TABLE `demo_object` (
      `id` bigint(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
      `user_info` json NOT NULL COMMENT '人员基础详情',
      `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
      `last_update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='测试对象表';
    INSERT INTO `demo_object`(`id`, `user_info`, `create_time`, `last_update_time`) VALUES (1, '{\"age\": 20, \"name\": \"xinjie\", \"comment\": \"this is comment1\", \"birthday\": \"1992-10-25\"}', '2021-11-30 14:36:21', '2021-11-30 15:41:30');
    """

    __tablename__ = "demo_object"

    userInfo = GenColumn(db.JSON, name="user_info", default=lambda: {}, comment="人员基础详情")

    def __init__(self, **kwargs):
        self.userInfo = kwargs.get("userInfo", {})
        TableMixin.__init__(self, **kwargs)
