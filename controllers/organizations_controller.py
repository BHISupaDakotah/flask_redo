from flask import request, jsonify
from modals.organizations import Organizations, organization_schema, organizations_schema
from db import db


def populate_object(obj, data_dictionary):
    print("\n=== Populate Object Debug ===")
    print(f"Object Type: {type(obj)}")
    print(f"Incoming Data: {data_dictionary}")

    # Get all attributes that exist in the model
    model_attrs = [attr for attr in dir(obj) if not attr.startswith('_')]
    print(f"Available Model Attributes: {model_attrs}")

    # Only update fields that exist in both the data and model
    for field in data_dictionary:
        if field in model_attrs and hasattr(obj, field):
            print(f"Updating {field}: {
                  getattr(obj, field)} -> {data_dictionary[field]}")
            setattr(obj, field, data_dictionary[field])
        else:
            print(f"Skipping field {field}: Not a valid model attribute")

    print("=== Update Complete ===\n")
    return obj


def organization_add():
    post_data = request.get_json()
    if not post_data:
        post_data = request.form

    # Create empty organization and populate it
    new_organization = Organizations()
    populate_object(new_organization, post_data)

    try:
        db.session.add(new_organization)
        db.session.commit()
        return jsonify({"message": "organization added", "result": organization_schema.dump(new_organization)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400


def organization_update(org_id):
    organization = db.session.query(Organizations).filter(
        Organizations.org_id == org_id).first()

    if not organization:
        return jsonify({'message': 'Organization not found'}), 404

    post_data = request.get_json()
    if not post_data:
        post_data = request.form

    populate_object(organization, post_data)

    try:
        db.session.commit()
        return jsonify({"message": "organization updated", "result": organization_schema.dump(organization)}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 400


def get_all_active_organizations():
    organizations = db.session.query(Organizations).filter(
        Organizations.active == True).all()

    if organizations:
        return jsonify({"message": "organizations found", "results": organizations_schema.dump(organizations)}), 200
    else:
        return jsonify({"message": "no organizations found"}), 404
