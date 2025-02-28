from controllers.users_controller import UsersController
from routes.base_routes import BaseRoutes

users_routes = BaseRoutes('user', UsersController)
