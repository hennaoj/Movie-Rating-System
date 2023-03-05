import json
from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from werkzeug.exceptions import NotFound, BadRequest, UnsupportedMediaType

from review_system import db
from review_system.models import Movie, Genre, Review

class MovieCollection(Resource):

    def get(self):
        movies = Movie.query.all()
        json_movies = []
        for movie in movies:
            json_movies.append(movie.Serialize())
        return Response(json.dumps(json_movies), 200)
    
    def post(self):
        if not request.json:
            return UnsupportedMediaType
        requestdict = json.loads(request.json)
        try:
            validate(requestdict, Movie.json_schema())
        except ValidationError as error:
            print(error)
            raise BadRequest(description=str(error)) from error
        
        requestdict = json.loads(request.json)

        movie_genres = []
        try:
            given_genres = requestdict["genres"]
            db_genres = [genre.name for genre in Genre.query.all()]

            for genre in given_genres:
                # creating a new genre object or fetching an existing one if the
                # genre name is found in the database
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
            title=requestdict["title"],
            release_year=requestdict["release_year"],
            genres=movie_genres
        )

        db.session.add(movie)
        db.session.commit()
        return Response(status=201, headers={
            "Location": url_for("movieitem", movie=movie)
        })

class MovieItem(Resource):

    def get(self, movie):
        return Response(json.dumps(movie.Serialize()), 200)
    
    def put(self, movie):
        if not request.json:
            return UnsupportedMediaType
        else:
            requestdict = json.loads(request.json)
        movie_genres = []
        try:
            given_genres = requestdict["genres"]
            db_genres = [genre.name for genre in Genre.query.all()]

            for genre in given_genres:
                # creating a new genre object or fetching an existing one if the
                # genre name is found in the database
                if genre not in db_genres:
                    genre_to_add = Genre(
                        name=genre
                    )
                else:
                    genre_to_add = Genre.query.filter_by(name=genre).first()
                movie_genres.append(genre_to_add)
        except KeyError:
            pass
        updatedict = {}
        try:
            updatedict["title"] = requestdict["title"]
        except:
            pass
        try:
            updatedict["release_year"] = requestdict["release_year"]
        except:
            pass
        if len(movie_genres) > 0:
            updatedict["genres"] = movie_genres
        updatecount = Movie.query.filter_by(id=movie.id).update(updatedict)
        db.session.commit() 
    
    def delete(self, movie):
        pass
