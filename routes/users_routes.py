from flask import Blueprint, request, jsonify
from modals.users import Users, user_schema, users_schema
from db import db


users = Blueprint('users', __name__)


@users.route('/user/add', methods=['POST'])
def user_add():
    post_data = request.json
    if not post_data:
        post_data = request.form

    first_name = post_data.get('first_name')
    last_name = post_data.get('last_name')
    email = post_data.get('email')
    phone = post_data.get('phone')
    city = post_data.get('city')
    state = post_data.get('state')
    org_id = post_data.get('org_id')
    active = post_data.get('active')

    new_user = Users(first_name, last_name, email,
                     phone, city, state, org_id, active)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(user_schema.dump(new_user)), 200


@users.route('/user/get/<user_id>', methods=['GET'])
def user_get(user_id):
    user = db.session.query(Users).filter(Users.user_id == user_id).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify(user_schema.dump(user)), 200


@users.route('/users/get', methods=['GET'])
def get_all_active_users():
    users = db.session.query(Users).filter(Users.active == True).all()

    return jsonify({"results": users_schema.dump(users)}), 200


@users.route('/user/update/<user_id>', methods=['PUT', 'POST'])
def user_update(user_id):
    user = db.session.query(Users).filter(Users.user_id == user_id).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    post_data = request.json
    if not post_data:
        post_data = request.form

    if post_data.get('first_name'):
        user.first_name = post_data.get('first_name')
    if post_data.get('last_name'):
        user.last_name = post_data.get('last_name')
    if post_data.get('email'):
        user.email = post_data.get('email')
    if post_data.get('phone'):
        user.phone = post_data.get('phone')
    if post_data.get('city'):
        user.city = post_data.get('city')
    if post_data.get('state'):
        user.state = post_data.get('state')
    if post_data.get('org_id'):
        user.org_id = post_data.get('org_id')
    if 'active' in post_data:
        user.active = post_data.get('active')

    db.session.commit()
    return jsonify(user_schema.dump(user)), 200


@users.route('/users/get/<org_id>', methods=['GET'])
def get_users_by_org_id(org_id):
    users = db.session.query(Users).filter(Users.org_id == org_id).all()
    return jsonify({"results": users_schema.dump(users)}), 200
