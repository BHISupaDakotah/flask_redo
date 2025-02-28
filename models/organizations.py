import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma


class OrganizationsSchema(ma.Schema):
    class Meta:
        fields = ('org_id', 'name', 'phone', 'city', 'state', 'active')


class Organizations(db.Model):

    __tablename__ = 'organizations'

    org_id = db.Column(UUID(as_uuid=True),
                       primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    users = db.relationship('Users', back_populates='organization', lazy=True)

    schema = OrganizationsSchema()

    @classmethod
    def create_empty_record(cls):
        return cls()
