from flask_restful import Api

from app import app
from resources.movie import MovieCollection, MovieItem

api = Api(app)

api.add_resource(MovieCollection, "/api/movies/")
api.add_resource(MovieItem, "/api/movies/<id>/")