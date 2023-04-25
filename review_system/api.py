'''Api related functionality'''
from review_system.resources.movie import MovieCollection, MovieItem
from review_system.resources.review import ReviewCollection, ReviewItem
from review_system.resources.genre import GenreCollection, GenreItem
from review_system.utils import MovieConverter, GenreConverter

def add_url_map_converters(app):
    '''Add url map converters to the application'''
    app.url_map.converters["movie"] = MovieConverter
    app.url_map.converters["genre"] = GenreConverter

def add_api_resources(api):
    '''Add resources to the api'''
    api.add_resource(MovieCollection, "/api/movies/")
    api.add_resource(MovieItem, "/api/movies/<movie:movie>/")
    api.add_resource(ReviewCollection, "/api/movies/<movie:movie>/reviews/")
    api.add_resource(ReviewItem, "/api/movies/<movie:movie>/reviews/<int:review>/")
    api.add_resource(GenreCollection, "/api/movies/genres/")
    api.add_resource(GenreItem, "/api/movies/genres/<genre:genre>/")
