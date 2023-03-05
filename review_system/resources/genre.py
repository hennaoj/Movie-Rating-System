import json
from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from werkzeug.exceptions import NotFound, BadRequest, UnsupportedMediaType

from review_system import db
from review_system.models import Movie, Genre, Review

class GenreCollection(Resource):

    def get(self):
        genres = Genre.query.all()
        json_genres = []
        for genre in genres:
            json_genres.append({
                "name": genre.name
            })
        return Response(json.dumps(json_genres), 200)
    
    def post(self):
        try:
            if not request.json:
                return Response(status=415)
            requestdict = json.loads(request.json)
        except:
            return Response(status=415)
        try:
            validate(requestdict, Genre.json_schema())
        except ValidationError as error:
            raise BadRequest(description=str(error)) from error
        genre = Genre(name=json.loads(request.json)["name"])
        db.session.add(genre)
        db.session.commit()
        return Response(status=201, headers={
            "Location": url_for("genreitem", genre=genre)
        })


class GenreItem(Resource):

    def get(self, genre):
        movieslist = []
        for movie in genre.movies:
            movieslist.append(movie.title)
        moviesingenredict = {'genre': genre.name, 'movies': movieslist}
        return Response(json.dumps(moviesingenredict), 200)
    
    def put(self, genre):
        pass
    
    def delete(self, genre):
        pass
