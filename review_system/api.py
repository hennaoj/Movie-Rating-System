from flask_restful import Api

from app import app
from resources.movie import MovieCollection, MovieItem
from resources.review import ReviewCollection, ReviewItem
from resources.genre import GenreCollection, GenreItem

api = Api(app)

api.add_resource(MovieCollection, "/api/movies/")
api.add_resource(MovieItem, "/api/movies/<int:movie>/")
api.add_resource(ReviewCollection, "/api/movies/<int:movie>/reviews/")
api.add_resource(ReviewItem, "/api/movies/<int:movie>/reviews/<int:review>/")
api.add_resource(GenreCollection, "/api/genres/")
api.add_resource(GenreItem, "/api/genres/<int:genre>/")