from controllers.organizations_controller import OrganizationsController
from routes.base_routes import BaseRoutes

organizations_routes = BaseRoutes('organization', OrganizationsController)
