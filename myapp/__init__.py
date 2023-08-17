import os

from flask import Flask 

from .extensions import db
from .routes import app


def create_app():

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://notesai_user:LS9drpA2s84V7RDtkCwuWwDKJTSl3C78@dpg-cjeh0egcfp5c73en5s40-a.ohio-postgres.render.com/notesai'
    #'sqlite:///users.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
    # app.run(host = "0.0.0.0", port=6969, debug=True)
    return app