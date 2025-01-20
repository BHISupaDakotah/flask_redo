import json
from flask import Flask, jsonify, request

from db import db, init_db
from users import Users
from organizations import Organizations
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dakotahholmes:postgres@localhost:5432/flask_redo'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app, db)


def create_all():
    with app.app_context():
        print("Creating all tables")
        db.create_all()
        print("All tables created!!!")

# user routes


@app.route('/user/add', methods=['POST'])
def user_add():
    post_data = request.json
    if not post_data:
        post_data = request.form
    print(post_data)

    first_name = post_data.get('first_name')
    last_name = post_data.get('last_name')
    email = post_data.get('email')
    phone = post_data.get('phone')
    city = post_data.get('city')
    state = post_data.get('state')
    org_id = post_data.get('org_id')
    active = post_data.get('active')

    add_user(first_name, last_name, email, phone, city, state, org_id, active)

    return jsonify({'message': 'User added successfully'}), 200


def add_user(first_name, last_name, email, phone, city, state, org_id, active):
    new_user = Users(first_name, last_name, email,
                     phone, city, state, org_id, active)

    db.session.add(new_user)
    db.session.commit()


@app.route('/user/get/<user_id>', methods=['GET'])
def user_get(user_id):
    user = db.session.query(Users).filter(Users.user_id == user_id).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user_data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone': user.phone,
        'city': user.city,
        'state': user.state,
        'organization': {
            'org_id': user.organization.org_id,
            'name': user.organization.name,
            'phone': user.organization.phone,
            'city': user.organization.city,
            'state': user.organization.state,
            'active': user.organization.active
        },
        'active': user.active
    }
    return jsonify(user_data), 200


@app.route('/users/get', methods=['GET'])
def get_all_active_users():
    users = db.session.query(Users).filter(Users.active == True).all()
    user_list = []

    for user in users:
        new_user = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.phone,
            'city': user.city,
            'state': user.state,
            'organization': {
                'org_id': user.organization.org_id,
                'name': user.organization.name,
                'phone': user.organization.phone,
                'city': user.organization.city,
                'state': user.organization.state,
                'active': user.organization.active
            },
            'active': user.active
        }
        user_list.append(new_user)
    return jsonify(user_list), 200


# organization routes


@app.route('/organization/add', methods=['POST'])
def organization_add():
    post_data = request.json
    if not post_data:
        post_data = request.form
    print(post_data)

    name = post_data.get('name')
    phone = post_data.get('phone')
    city = post_data.get('city')
    state = post_data.get('state')
    active = post_data.get('active')

    add_organization(name, phone, city, state, active)

    return jsonify({'message': 'Organization added successfully'}), 200


def add_organization(name, phone, city, state, active):
    new_organization = Organizations(name, phone, city, state, active)

    db.session.add(new_organization)
    db.session.commit()


if __name__ == '__main__':
    create_all()
    app.run(host='0.0.0.0', port=8086)
