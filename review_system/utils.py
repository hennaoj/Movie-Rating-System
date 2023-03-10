'''Miscellaneous utilities'''
from werkzeug.exceptions import NotFound
from werkzeug.routing import BaseConverter
from review_system.models import Movie, Genre, Review

class MovieConverter(BaseConverter):
    '''Converter for movies'''
    def to_python(self, value):
        db_movie = Movie.query.filter_by(id=value).first()
        if db_movie is None:
            raise NotFound
        return db_movie

    def to_url(self, value):
        return str(value.id)

class ReviewConverter(BaseConverter):
    '''Converter for reviews'''
    def to_python(self, value):
        db_review = Review.query.filter_by(id=value).first()
        if db_review is None:
            raise NotFound
        return db_review

    def to_url(self, value):
        return str(value.id)

class GenreConverter(BaseConverter):
    '''Converter for genres'''
    def to_python(self, value):
        db_genre = Genre.query.filter_by(id=value).first()
        if db_genre is None:
            raise NotFound
        return db_genre

    def to_url(self, value):
        return str(value.id)
    