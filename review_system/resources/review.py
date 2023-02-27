import json
from datetime import datetime
from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from werkzeug.exceptions import NotFound, BadRequest, UnsupportedMediaType

from models import db, Movie, User, Review

class ReviewCollection(Resource):

    def get(self, movie):
        reviews = Review.query.filter_by(movie_id=movie)
        json_reviews = []
        for review in reviews:
            json_reviews.append({
                "rating": review.rating,
                "comment": review.comment
            })
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
            movie_id=movie,
            user_id = 1 #this needs to be fixed, just a placeholder for now
        )

        db.session.add(review)
        db.session.commit()
        
        return Response(status=201, headers={
            "Location": url_for("reviewitem", movie=movie, review=review.id)
        })

class ReviewItem(Resource):

    def get(self, movie, review):
        pass
    
    def put(self, movie, review):
        pass
    
    def delete(self, movie, review):
        pass
