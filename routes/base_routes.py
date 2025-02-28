from flask import Blueprint


class BaseRoutes():

    def __init__(self, blueprint_name, controller):
        self.blueprint = Blueprint(blueprint_name, __name__)
        self.blueprint_name = blueprint_name
        self.controller = controller()

        self.blueprint.add_url_rule(
            f'/{blueprint_name}', "add", self.add, methods=["POST"])
        self.blueprint.add_url_rule(
            f'/{blueprint_name}s', "get_all", self.get_all, methods=["GET"])
        self.blueprint.add_url_rule(
            f'/{blueprint_name}/<record_id>', "get_by_id", self.get_by_id, methods=["GET"])
        self.blueprint.add_url_rule(
            f'/{blueprint_name}/<record_id>', "update", self.update, methods=["PUT"])
        self.blueprint.add_url_rule(
            f'/{blueprint_name}/delete/<record_id>', "delete", self.add, methods=["DELETE"])

    def add_route(self, route, endpoint, methods):
        if self.blueprint_name == 'auth':
            self.blueprint.add_url_rule(route, endpoint, getattr(
                self.controller, endpoint), methods=methods)
        else:
            self.blueprint.add_url_rule(
                f'/{self.blueprint_name}{route}', endpoint, getattr(self.controller, endpoint), methods=methods)

    def add(self):
        return self.controller.add()

    def get_all(self):
        return self.controller.get_all()

    def get_by_id(self, record_id):
        return self.controller.get_by_id(record_id)

    def update(self, record_id):
        return self.controller.update(record_id)

    def delete(self, record_id):
        return self.controller.delete(record_id)
