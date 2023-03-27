"""Movie resource module"""
import json

from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from review_system import db
from review_system.models import Movie, Genre
from review_system.auth import check_api_key
from review_system.constants import *
from review_system.utils import ReviewSystemBuilder

class MovieCollection(Resource):
    """Movie collection resource"""
    def get(self):
        movies = Movie.query.all()
        
        body = ReviewSystemBuilder()
        body["items"] = []
        body.add_namespace("revsys", LINK_RELATIONS_URL)
        body.add_control_add_movie()
        body.add_control("self", url_for("moviecollection"))

        for movie in movies:
            item = ReviewSystemBuilder(Movie.serialize(movie))
            item.add_control("self", url_for("movieitem", movie=movie))
            item.add_control("profile", MOVIE_PROFILE)
            body["items"].append(item)

        return Response(json.dumps(body), 200, mimetype=MASON)

    @check_api_key
    def post(self):
        try:
            requestdict = json.loads(request.data)
        except:
            return Response(status=415)
        
        try:
            validate(requestdict, Movie.json_schema())
        except ValidationError as error:
            print(error)
            raise BadRequest(description=str(error)) from error

        requestdict = json.loads(request.data)

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

        movies = Movie.query.all()
        uri_id = requestdict["title"].replace(" ", "").lower()

        title_occurences = 0
        for db_movie in movies:
            if db_movie.uri_id == uri_id:
                title_occurences += 1

        if title_occurences != 0:
            uri_id = uri_id + "_{}".format(title_occurences)

        movie = Movie(
            title=requestdict["title"],
            release_year=requestdict["release_year"],
            genres=movie_genres,
            uri_id=uri_id
        )

        db.session.add(movie)
        db.session.commit()
        
        return Response(status=201, headers={
            "Location": url_for("movieitem", movie=movie)
        })

class MovieItem(Resource):
    """Movie item resource"""
    def get(self, movie):
        body = ReviewSystemBuilder(movie.serialize())
        body.add_namespace("revsys", LINK_RELATIONS_URL)
        body.add_control_delete_movie(movie)
        body.add_control("self", url_for("movieitem",  movie=movie))
        body.add_control("profile", MOVIE_PROFILE)
        body.add_control("collection", url_for("moviecollection"))
        body.add_control("reviews", url_for("reviewcollection", movie=movie))
        try:
            return Response(json.dumps(body), 200, mimetype=MASON)
        except:
            return Response(status=404)

    def put(self, movie):
        try:
            if not request.json:
                return Response(status=415)
            else:
                requestdict = json.loads(request.json)
        except:
            return Response(status=415)
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
            updatedict["release_year"] = requestdict["release_year"]
        except:
            pass
        if len(movie_genres) > 0:
            updatedict["genres"] = movie_genres
        updatecount = Movie.query.filter_by(id=movie.id).update(updatedict)
        db.session.commit()
        return Response(status=204)

    def delete(self, movie):
        Movie.query.filter_by(id=movie.id).delete()
        db.session.commit()
        return Response(status=200)
