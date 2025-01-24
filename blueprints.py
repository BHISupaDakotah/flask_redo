from routes import *


def register_blueprints(app):
    app.register_blueprint(organizations)
    app.register_blueprint(users)
