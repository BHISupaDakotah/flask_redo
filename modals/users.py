import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma
from modals.organizations import OrganizationsSchema


class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(UUID(as_uuid=True),
                        primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey(
        'organizations.org_id'), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    organization = db.relationship('Organizations', back_populates='users')

    def __init__(self, first_name, last_name, email, phone, city, state, org_id, active):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.city = city
        self.state = state
        self.org_id = org_id
        self.active = active


class UsersSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'first_name', 'last_name', 'email',
                  'phone', 'city', 'state', 'organization', 'active')

    organization = ma.fields.Nested(OrganizationsSchema())


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)
