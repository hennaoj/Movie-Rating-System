import json
from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from werkzeug.exceptions import NotFound, BadRequest, UnsupportedMediaType

from models import db, Movie, Genre, Review

class MovieCollection(Resource):

    def get(self):
        movies = Movie.query.all()
        json_movies = []
        for movie in movies:
            json_movies.append({
                "title": movie.title,
                "release_year": movie.release_year,
                "average_rating": movie.average_rating
            })
        return Response(json.dumps(json_movies), 200)
    
    def post(self):
        if not request.json:
            return UnsupportedMediaType
        try:
            validate(request.json, Movie.json_schema())
        except ValidationError as error:
            raise BadRequest(description=str(error)) from error


        movie_genres = []
        try:
            given_genres = request.json["genres"]
            db_genres = [genre.name for genre in Genre.query.all()]

            for genre in given_genres:
                #creating a new genre object or fetching an existing one if the
                #genre name is found in the database
                if genre not in db_genres:
                    genre_to_add = Genre(
                        name=genre
                    )
                else:
                    genre_to_add = Genre.query.filter_by(name=genre).first()
                movie_genres.append(genre_to_add)
            
        except KeyError:
            pass


        movie = Movie(
            title=request.json["title"],
            release_year=request.json["release_year"],
            genres=movie_genres
        )

        db.session.add(movie)
        db.session.commit()
        
        return Response(status=201, headers={
            "Location": url_for("movieitem", id=movie.id)
        })

class MovieItem(Resource):

    def get(self, movie):
        pass
    
    def put(self, movie):
        pass
    
    def delete(self, movie):
        pass
