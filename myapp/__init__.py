import os

from flask import Flask 

from .extensions import db
from .routes import app


def create_app(database_uri= os.environ["DATABASE_URL"]):

    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    #'sqlite:///users.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
    # app.run(host = "0.0.0.0", port=6969, debug=True)
    return app

def create_app_testing(database_uri= os.environ["DATABASE_URL"]):

    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    #'sqlite:///users.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if 'sqlalchemy' not in app.extensions:
        db.init_app(app)

    with app.app_context():
        db.create_all()
    # app.run(host = "0.0.0.0", port=6969, debug=True)
    return app