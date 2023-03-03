from flask_restful import Api

from app import app
from resources.movie import MovieCollection, MovieItem
from resources.review import ReviewCollection, ReviewItem
from resources.genre import GenreCollection, GenreItem
from utils import MovieConverter, ReviewConverter

app.url_map.converters["movie"] = MovieConverter
app.url_map.converters["review"] = ReviewConverter

api = Api(app)

api.add_resource(MovieCollection, "/api/movies/")
api.add_resource(MovieItem, "/api/movies/<movie:movie>/")
api.add_resource(ReviewCollection, "/api/movies/<movie:movie>/reviews/")
api.add_resource(ReviewItem, "/api/movies/<movie:movie>/reviews/<review:review>/")
api.add_resource(GenreCollection, "/api/genres/")
api.add_resource(GenreItem, "/api/genres/<int:genre>/")