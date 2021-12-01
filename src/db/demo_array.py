# -*- coding: utf-8 -*-

from src.db.base import (
    db,
    TableMixin,
    GenColumn)


class DemoArrayModel(db.Model, TableMixin):
    """demo_array
    CREATE TABLE `demo_array` (
      `id` bigint(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
      `edu_list` json NOT NULL COMMENT '教育列表',
      `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
      `last_update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='测试列表表';
    INSERT INTO `demo_array`(`id`, `edu_list`, `create_time`, `last_update_time`) VALUES (1, '[{\"major\": \"搓泥1\", \"school\": \"北大\"}, {\"major\": \"清华池\", \"school\": \"清华\"}]', '2021-11-30 16:42:11', '2021-12-01 11:35:05');
    INSERT INTO `demo_array`(`id`, `edu_list`, `create_time`, `last_update_time`) VALUES (2, '[{\"major\": \"搓泥1\", \"school\": \"北大1\"}]', '2021-11-30 16:43:39', '2021-11-30 19:03:00');
    """

    __tablename__ = "demo_array"

    eduList = GenColumn(db.JSON, name="edu_list", default=lambda: [], comment="教育列表")

    def __init__(self, **kwargs):
        self.eduList = kwargs.get("eduList", [])
        TableMixin.__init__(self, **kwargs)
