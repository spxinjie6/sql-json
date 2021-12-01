from sqlalchemy import func

from src.db.base import db
from src.api.base import ApiResource
from src.db.demo_object import DemoObjectModel
from src.db.demo_array import DemoArrayModel


class DemoObjectHandler(ApiResource):
    """
    json object 操作
    """

    def get(self):
        """获取json object keys

        select id,
        replace(JSON_EXTRACT(user_info, '$.age'), '"', '') as age,
        replace(JSON_EXTRACT(user_info, '$.birthday'), '"', '') as birthday
        from demo_object
        where JSON_EXTRACT(user_info, '$.name') = '$name';
        """
        self.add_argument("name", type=str, location="args", required=True, help="name is required")
        args = self.parse_args()
        models = DemoObjectModel.query.filter(
            DemoObjectModel.userInfo["name"] == args.get("name")
        ).with_entities(
            DemoObjectModel.id,
            func.replace(
                func.json_extract(
                    DemoObjectModel.userInfo, '$.age'
                ), '"', ''
            ).label("age"),
            func.replace(
                func.json_extract(
                    DemoObjectModel.userInfo, '$.birthday'
                ), '"', ''
            ).label("birthday")
        )
        data = []
        for model in models:
            data.append(dict(
                id=model.id,
                age=model.age,
                birthday=model.birthday,
            ))
        return self.make_ok(dict(data=data))

    def post(self):
        body = self.parse_json({
            "type": "object",
            "properties": {
                "userInfo": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "number"},
                        "birthday": {"type": "string"},
                    },
                    "required": [
                        "name",
                        "age",
                        "birthday"
                    ]
                }
            },
            "required": ["userInfo"]
        })
        with db.session.begin(subtransactions=True) as s:
            s.session.add(DemoObjectModel(**body))
        return self.make_ok()

    def put(self):
        """针对字段更新(key 不存在json object 增加key)

        UPDATE demo_object
        set
        user_info = JSON_SET(user_info, '$.comment', '$comment')
        where
        JSON_EXTRACT(user_info, '$.name') = '$name';
        """
        body = self.parse_json({
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "comment": {"type": "string"}
            },
            "required": ["name"]
        })
        comment = body.get("comment", "")
        if not comment:
            return self.make_ok()
        DemoObjectModel.query.filter(
            DemoObjectModel.userInfo["name"] == body.get("name")
        ).update(
            {"userInfo": func.json_set(DemoObjectModel.userInfo, '$.comment', comment)},
            synchronize_session='fetch'
        )
        return self.make_ok()

    def delete(self):
        """删除json 中的某个key

        查询key 是否存在
        SELECT json_contains_path(`user_info`, 'all', '$.comment')  from `demo_object` WHERE
        JSON_EXTRACT(user_info, '$.name') = '$name';
        UPDATE demo_object set user_info = JSON_REMOVE(user_info, '$.comment’)
        where JSON_EXTRACT(user_info, '$.name') = '$name';
        """
        body = self.parse_json({
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "key": {"type": "string"}
            },
            "required": ["name", "key"]
        })
        query_model = DemoObjectModel.query.filter(
            DemoObjectModel.userInfo["name"] == body.get("name")
        )
        key = body.get('key')
        is_has_keys = query_model.with_entities(
            func.json_contains_path(
                DemoObjectModel.userInfo,
                "all",
                f"$.{key}"
            ).label("exist")
        ).first().exist
        if is_has_keys:
            query_model.update(
                {"userInfo": func.json_remove(DemoObjectModel.userInfo, f'$.{key}')},
                synchronize_session='fetch'
            )
        return self.make_ok()


class DemoArrayHandler(ApiResource):
    """json array 操作
    根据school 获取 major

    SELECT
    id,
    JSON_EXTRACT(edu_list,
    REPLACE(REPLACE(JSON_SEARCH(edu_list, 'all', '北大'),'"',''),'.school','.major')) as major
    from demo_array;
    """

    def get(self):
        self.add_argument("school", type=str, location="args", required=True, help="school is required")
        args = self.parse_args()
        school = args.get("school", "")
        models = DemoArrayModel.query.filter().with_entities(
            DemoArrayModel.id,
            func.replace(
                func.json_extract(DemoArrayModel.eduList, func.replace(
                    func.replace(
                        func.json_search(
                            DemoArrayModel.eduList,
                            'all',
                            school
                        ), '"', ''
                    ), '.school', '.major')), '"', ''
            ).label("major")
        )
        data = []
        for model in models:
            data.append(dict(
                id=model.id,
                major=model.major
            ))
        return self.make_ok(dict(data=data))

    def post(self):
        body = self.parse_json(dict(
            type="object",
            properties=dict(
                properties=dict(
                    eduList=dict(
                        type="array",
                        items=dict(
                            type="object",
                            properties=dict(
                                school=dict(type="string"),
                                major=dict(type="string")
                            ),
                            required=["school", "major"]
                        )
                    )
                )
            ),
            required=["eduList"]
        ))
        with db.session.begin(subtransactions=True) as s:
            s.session.add(DemoArrayModel(**body))
        return self.make_ok()

    def put(self):
        """ 修改
        update demo_array
        set edu_list =
        JSON_REPLACE(edu_list, replace(JSON_SEARCH(edu_list, 'all', '北京大学'), '"', ''), '北大');
        """
        body = self.parse_json(dict(
            type="object",
            properties=dict(
                newSchool=dict(type="string"),
                oldSchool=dict(type="string")
            ),
            required=["newSchool", "oldSchool"]
        ))
        DemoArrayModel.query.filter().update(
            {"eduList": func.json_replace(
                DemoArrayModel.eduList,
                func.replace(
                    func.json_search(
                        DemoArrayModel.eduList,
                        'all',
                        body.get('oldSchool')
                    ),
                    '"',
                    ''
                ),
                body.get("newSchool")
            )},
            synchronize_session='fetch'
        )
        return self.make_ok()

    def delete(self):
        """根据school 删除 major

        查询key 是否存在
        SELECT JSON_CONTAINS_PATH(edu_list, 'one',
        REPLACE(JSON_SEARCH(edu_list, 'one', '北大', null, '$**.school'),'"','')
        ) from demo_array;
        存在删除major key
        update demo_array set
        edu_list = JSON_REMOVE(
            edu_list,
            REPLACE(
                REPLACE(
                    JSON_SEARCH(
                        edu_list, 'one', '北大'
                    ),
                '"',
                ''),
            '.school',
            '.major')
        ) where id=1;
        """
        models = DemoArrayModel.query.filter().with_entities(
            DemoArrayModel.id,
            func.json_contains_path(
                DemoArrayModel.eduList,
                'one',
                func.replace(
                    func.json_search(
                        DemoArrayModel.eduList,
                        'one',
                        '北大',
                        None,
                        '$**.school'
                    ), '"', ''
                )
            ).label("count")
        )
        exist_ids = []
        for model in models:
            if model.count:
                exist_ids.append(model.id)
        if exist_ids:
            DemoArrayModel.query.filter(
                DemoArrayModel.id.in_(exist_ids)
            ).update(
                {"eduList": func.json_remove(
                    DemoArrayModel.eduList,
                    func.replace(
                        func.replace(
                            func.json_search(
                                DemoArrayModel.eduList,
                                'all',
                                '北大'
                            ),
                            '"',
                            ''
                        ),
                        '.school',
                        '.major'
                    )
                )},
                synchronize_session='fetch'
            )
        return self.make_ok()
