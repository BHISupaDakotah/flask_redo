from flask import Blueprint, request, jsonify
from modals.organizations import Organizations, organization_schema, organizations_schema
from db import db
from controllers import organizations_controller

organizations = Blueprint('organizations', __name__)


@organizations.route('/organization', methods=['POST'])
def organization_add():
    return organizations_controller.organization_add()


@organizations.route('/organization/<org_id>', methods=['PUT'])
def organization_update(org_id):
    return organizations_controller.organization_update(org_id)


@organizations.route('/organizations/active', methods=['GET'])
def get_all_active_organizations():
    return organizations_controller.get_all_active_organizations()
