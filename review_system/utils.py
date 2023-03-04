from werkzeug.exceptions import NotFound
from werkzeug.routing import BaseConverter
from models import Movie, Review, Genre

class MovieConverter(BaseConverter):
    
    def to_python(self, movie_id):
        db_movie = Movie.query.filter_by(id=movie_id).first()
        if db_movie is None:
            raise NotFound
        return db_movie
        
    def to_url(self, db_movie):
        return db_movie.id

class ReviewConverter(BaseConverter):
    
    def to_python(self, review_id):
        db_review = Review.query.filter_by(id=review_id).first()
        if db_review is None:
            raise NotFound
        return db_review
        
    def to_url(self, db_review):
        return db_review.id
    
class GenreConverter(BaseConverter):
    
    def to_python(self, genre_id):
        db_genre = Genre.query.filter_by(id=genre_id).first()
        if db_genre is None:
            raise NotFound
        return db_genre
        
    def to_url(self, db_genre):
        return db_genre.id
    