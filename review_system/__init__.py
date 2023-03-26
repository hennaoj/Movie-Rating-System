"""Flask-based review system for movies"""
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

from review_system.constants import *

db = SQLAlchemy()

def create_app(test_config=None):
    '''Creates the flask application'''
    app = Flask(__name__, instance_relative_config=True)
    api_ = Api()

    dbpath = os.path.join(app.instance_path, "movie_rating_system.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + dbpath
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is not None:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    from review_system import models
    app.cli.add_command(models.init_db_command)
    from review_system import create_sample_data
    app.cli.add_command(create_sample_data.create_sample_data)
    from review_system import create_sample_api_key
    app.cli.add_command(create_sample_api_key.create_sample_api_key)
    from review_system import api
    api.add_url_map_converters(app)
    api.add_api_resources(api_)
    api_.init_app(app)

    @app.route(LINK_RELATIONS_URL)
    def view_link_relations():
        return "link relations"

    @app.route("/profiles/<profile>/")
    def view_profile(profile):
        return "this is the {} profile".format(profile)

    return app
