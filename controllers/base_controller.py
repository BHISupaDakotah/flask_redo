import json

from flask import request, jsonify, make_response, current_app, abort
from helpers.controller_helpers import get_record
from models import *
from db import db
from sqlalchemy.orm import sessionmaker


class BaseController:
    model = None

    def forbidden_table(self, table_name):
        if self.model.__tablename__ == table_name:
            response = make_response(jsonify(
                {"message": "you are not authorized to perform this action on this table"}), 403)
            abort(response)

    def populate_object(self, obj, data_dictionary):
        if hasattr(obj, 'UPDATABLE_COLUMNS'):
            invalid_columns = [field for field in data_dictionary if field in obj.__table__.columns.keys(
            ) and field not in obj.UPDATABLE_COLUMNS]
            if invalid_columns:
                response = make_response(jsonify({
                    "message": f"Cannot update columns: {', '.join(invalid_columns)}. Only {', '.join(obj.UPDATABLE_COLUMNS)} can be updated."
                }), 400)
                abort(response)

        for field in data_dictionary:
            if hasattr(obj, field):
                setattr(obj, field, data_dictionary[field])
            else:
                response = make_response(jsonify({
                    "message": f"no '{field}' column in {self.model.__tablename__} table."
                }), 400)
                abort(response)

    def commit(self):
        """Commit database changes"""
        try:
            db.session.commit()
        except Exception as e:
            print("commit error: ", e)
            db.session.rollback()
            error_message = str(e)

            if "psycopg2.errors.UniqueViolation" in error_message:
                error_message = error_message.split(")")[1].split('"')
                error_message = f"{error_message[0]}'{error_message[1]}'"
                response = make_response(jsonify(
                    {"message": f"unable to commit changes to database.{error_message}"}), 400)
                abort(response)
            else:
                response = make_response(
                    jsonify({"message": f"unable to commit changes to database."}), 400)
                abort(response)

    # @authenticate_return_user
    def add(self):
        # self.forbidden_table("bAPVM")

        post_data = request.form if request.form else request.json
        new_record = self.model.create_empty_record()

        self.populate_object(new_record, post_data)
        db.session.add(new_record)

        # self.log_operation('INSERT', record_name=self.get_record_name(
        #     new_record), new_values=post_data, user_email=user_info.get('email'))

        self.commit()

        return jsonify({"message": "record added", "result": self.model.schema.dump(new_record)}), 201

    # @authenticate
    def get_all(self):
        all_records = self.model.query.all()

        return jsonify({"message": "record(s) found", "results": self.model.schema.dump(all_records, many=True)}), 200

        # @authenticate
    def get_by_id(self, record_id):
        record = get_record(self.model, record_id)

        return jsonify({"message": "record found", "result": self.model.schema.dump(record)}), 200

    #  @authenticate_return_user
    # def update(self, record_id, user_info):
    def update(self, record_id):
        # self.forbidden_table("bAPVM")
        post_data = request.form if request.form else request.json
        record = get_record(self.model, record_id)

        old_values = self.model.schema.dump(record)

        self.populate_object(record, post_data)

        # self.log_operation('UPDATE', record_id=record_id, record_name=self.get_record_name(
        #     record), old_values=old_values, new_values=post_data, user_email=user_info.get('email'))

        self.commit()

        return jsonify({"message": "record updated", "result": self.model.schema.dump(record)}), 200

    # @authenticate_return_user
    # def delete(self, record_id, user_info):
    def delete(self, record_id):
        # self.forbidden_table("bAPVM")

        record = get_record(self.model, record_id)

        old_values = self.model.schema.dump(record)

        if "test" in self.model.__tablename__.lower():

            db.session.delete(record)

            # self.log_operation('DELETE', record_id=record_id, record_name=self.get_record_name(
            #     record), old_values=old_values, user_email=user_info.get('email'))

            self.commit()

            return jsonify({"message": "record deleted", "result": self.model.schema.dump(record)}), 200
        else:
            return jsonify({"message": "unable to delete record"}), 400

    def get_record_name(self, record):
        """
        Gets all columns in a table that have 'name' as a substring in their name (case-insensitive)
        and concatenates their values with spaces between them.

        Args:
            record: The database record to get values from

        Returns:
            str: Space-separated string of values from name-related columns
        """

        columns = record.__table__.columns.keys()

        name_columns = [col for col in columns if 'name' in col.lower()]

        values_dict = {col: getattr(record, col) for col in name_columns if getattr(
            record, col) is not None}

        return values_dict
