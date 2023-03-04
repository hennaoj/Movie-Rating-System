import json
from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from werkzeug.exceptions import NotFound, BadRequest, UnsupportedMediaType

from models import db, Genre

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
        return Response(json.dumps(Genre.Serialize(genre)), 200)
    
    def put(self, genre):
        pass
    
    def delete(self, genre):
        pass
