import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma
from models.organizations import OrganizationsSchema


class UsersSchema(ma.Schema):

    class Meta:
        fields = ('user_id', 'first_name', 'last_name', 'email',
                  'phone', 'city', 'state', 'organization', 'active')

    organization = ma.fields.Nested(OrganizationsSchema())


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
    organization = db.relationship(
        'Organizations', back_populates='users', lazy=True)

    schema = UsersSchema()

    @classmethod
    def create_empty_record(cls):
        return cls()
