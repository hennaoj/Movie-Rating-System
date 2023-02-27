import json
from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from werkzeug.exceptions import NotFound, BadRequest, UnsupportedMediaType

from models import db, Movie, User, Genre, Review

class ReviewCollection(Resource):

    def get(self):
        pass
    
    def post(self):
        pass

class ReviewItem(Resource):

    def get(self, movie):
        pass
    
    def put(self, movie):
        pass
    
    def delete(self, movie):
        pass
