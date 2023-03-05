from review_system.resources.movie import MovieCollection, MovieItem
from review_system.resources.review import ReviewCollection, ReviewItem
from review_system.resources.genre import GenreCollection, GenreItem
from review_system.utils import MovieConverter, ReviewConverter, GenreConverter

def AddUrlMapConverters(app):
	app.url_map.converters["movie"] = MovieConverter
	app.url_map.converters["genre"] = GenreConverter

def AddApiResources(api):
	api.add_resource(MovieCollection, "/api/movies/")
	api.add_resource(MovieItem, "/api/movies/<movie:movie>/")
	api.add_resource(ReviewCollection, "/api/movies/<movie:movie>/reviews/")
	api.add_resource(ReviewItem, "/api/movies/<movie:movie>/reviews/<int:review>/")
	api.add_resource(GenreCollection, "/api/genres/")
	api.add_resource(GenreItem, "/api/genres/<genre:genre>/")