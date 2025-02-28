from routes import *


def register_blueprints(app):
    app.register_blueprint(organizations_routes.blueprint)
    app.register_blueprint(users_routes.blueprint)
