import json
from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow

from db import db, init_db
from blueprints import register_blueprints

app = Flask(__name__)

register_blueprints(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dakotahholmes:postgres@localhost:5432/flask_redo'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app, db)


def create_all():
    with app.app_context():
        print("Creating all tables...")
        db.create_all()
        print("All tables created!!!")


if __name__ == '__main__':
    create_all()
    app.run(host='0.0.0.0', port=8086)
