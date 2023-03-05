import json
from datetime import datetime
from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from werkzeug.exceptions import NotFound, BadRequest, UnsupportedMediaType

from review_system import db
from review_system.models import Movie, User, Review


class ReviewCollection(Resource):

    def get(self, movie):
        reviews = Review.query.filter_by(movie_id=movie.id)
        json_reviews = []
        for review in reviews:
            json_reviews.append(Review.Serialize(review))
        return Response(json.dumps(json_reviews), 200)
    
    def post(self, movie):
        if not request.json:
            return UnsupportedMediaType
        try:
            validate(request.json, Review.json_schema())
        except ValidationError as error:
            raise BadRequest(description=str(error)) from error

        comment = None
        try:
            comment = request.json["comment"]
        except KeyError:
            pass

        review = Review(
            rating=request.json["rating"],
            comment=comment,
            date=datetime.now(),
            movie_id=movie.id,
            user_id = 1 # this needs to be fixed, just a placeholder for now
        )

        #average update needs to be added

        db.session.add(review)
        db.session.commit()
        
        return Response(status=201, headers={
            "Location": url_for("reviewitem", movie=movie, review=review.id)
        })

class ReviewItem(Resource):
    def get(self, movie, review):
        try:
            return Response(json.dumps(movie.reviews[review].Serialize()), 200)
        except:
            return Response(status=404)
    
    def put(self, movie, review):
        pass
    
    def delete(self, movie, review):
        pass
