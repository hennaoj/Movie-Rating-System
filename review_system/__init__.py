import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    api_ = Api()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(app.instance_path, "movie_rating_system.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    if test_config != None:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    db.init_app(app)
    from . import models
    app.cli.add_command(models.init_db_command)
    from . import create_sample_data
    app.cli.add_command(create_sample_data.create_sample_data)
    from . import api
    api.AddUrlMapConverters(app)
    api.AddApiResources(api_)
    api_.init_app(app)
    return app
