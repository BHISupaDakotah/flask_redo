from controllers.base_controller import BaseController
from models import Users


class UsersController(BaseController):
    model = Users
