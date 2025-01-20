from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

# from lib.loaders import load_config

# Export just the db and init_db symbols when 'from db import *' is used
__all__ = ('db', 'init_db')

# our global db object (imported by models and views)
db = SQLAlchemy()

# support importing a function session.query
query = db.session.query


def init_db(app=None, db=None):
    if isinstance(app, Flask) and isinstance(db, SQLAlchemy):
        # force_auto_coercion()
        # load_modals()
        db.init_app(app)

    else:
        raise ValueError(
            "app and db must be instances of Flask and SQLAlchemy")
