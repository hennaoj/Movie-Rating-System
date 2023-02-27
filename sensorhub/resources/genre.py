import json
from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from werkzeug.exceptions import NotFound, BadRequest, UnsupportedMediaType

from models import db, Movie, User, Genre, Review

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
        pass

class GenreItem(Resource):

    def get(self, genre):
        pass
    
    def put(self, genre):
        pass
    
    def delete(self, genre):
        pass
