from src.api.v1 import DemoMoudle


def init(restful_api):

    restful_api.add_resource(DemoMoudle.DemoObjectHandler, "/api/v1/demo/object",
                             methods=["GET", "POST", "PUT", "DELETE"])

    restful_api.add_resource(DemoMoudle.DemoArrayHandler, "/api/v1/demo/array",
                             methods=["POST", "GET", "PUT", "DELETE"])
