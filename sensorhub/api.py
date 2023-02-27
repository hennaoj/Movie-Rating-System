from flask_restful import Api

from app import app
from resources.movie import MovieCollection, MovieItem
from resources.review import ReviewCollection, ReviewItem
from resources.genre import GenreCollection, GenreItem

api = Api(app)

api.add_resource(MovieCollection, "/api/movies/")
api.add_resource(MovieItem, "/api/movies/<id>/")
api.add_resource(ReviewCollection, "/api/<int:movie>/reviews/")
api.add_resource(ReviewItem, "/api/<int:movie>/reviews/<id>/")
api.add_resource(GenreCollection, "/api/genres/")
api.add_resource(GenreItem, "/api/genres/<id>/")