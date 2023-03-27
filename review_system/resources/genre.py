"""Genre resource module"""
import json

from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from review_system import db
from review_system.models import Genre
from review_system.auth import check_api_key
from review_system.constants import *
from review_system.utils import ReviewSystemBuilder

class GenreCollection(Resource):
    """Genre collection resource"""
    def get(self):
        genres = Genre.query.all()
        
        body = ReviewSystemBuilder()
        body["items"] = []
        body.add_namespace("revsys", LINK_RELATIONS_URL)
        body.add_control_add_genre()
        body.add_control("self", url_for("genrecollection"))

        for genre in genres:
            item = ReviewSystemBuilder(genre.serialize())
            item.add_control("self", url_for("genreitem", genre=genre))
            body["items"].append(item)

        return Response(json.dumps(body), 200, mimetype=MASON)
    
    @check_api_key
    def post(self):
        try:
            requestdict = json.loads(request.data)
        except:
            return Response(status=415)
        try:
            validate(requestdict, Genre.json_schema())
        except ValidationError as error:
            raise BadRequest(description=str(error)) from error
        genre = Genre(name=json.loads(request.data)["name"])
        db.session.add(genre)
        db.session.commit()
        return Response(status=201, headers={
            "Location": url_for("genreitem", genre=genre)
        })


class GenreItem(Resource):
    """Genre item resource"""
    def get(self, genre):
        movieslist = []
        for movie in genre.movies:
            movieslist.append(movie.title)
        moviesingenredict = {'genre': genre.name, 'movies': movieslist}
        return Response(json.dumps(moviesingenredict), 200)
