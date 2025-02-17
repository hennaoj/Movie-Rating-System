"""Review resource module"""
import json
from datetime import datetime
from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from review_system import db
from review_system.models import Review, User, Apikey
from review_system.auth import check_api_key
from review_system.constants import *
from review_system.utils import ReviewSystemBuilder

class ReviewCollection(Resource):
    """Review collection resource"""
    def get(self, movie):
        reviews = Review.query.filter_by(movie_id=movie.id)

        body = ReviewSystemBuilder()
        body["items"] = []
        body.add_namespace("revsys", LINK_RELATIONS_URL)
        body.add_control_add_review(movie)
        body.add_control("self", url_for("reviewcollection", movie=movie))
        body.add_control("movie", url_for("movieitem", movie=movie))

        for idx, review in enumerate(reviews):
            item = ReviewSystemBuilder(Review.serialize(review))
            item.add_control("self", url_for("reviewitem",  movie=movie, review=idx))
            item.add_control("profile", REVIEW_PROFILE)
            body["items"].append(item)

        return Response(json.dumps(body), 200, mimetype=MASON)

    @check_api_key
    def post(self, movie):
        if not request.json:
            return Response(status=415)
        try:
            validate(request.json, Review.json_schema())
        except ValidationError as error:
            print(error)
            raise BadRequest(description=str(error)) from error

        comment = None
        try:
            comment = request.json["comment"]
        except KeyError:
            pass

        user_id = 1
        try:
            apikey = request.json["apikey"]
            user_id = Apikey.query.filter_by(key=apikey).first().user_id
        except KeyError as e:
            print(e)
            pass


        review = Review(
            rating=request.json["rating"],
            comment=comment,
            date=datetime.now(),
            movie_id=movie.id,
            user_id = user_id
        )

        #average update needs to be added

        db.session.add(review)
        movie.update_rating()
        db.session.commit()

        return Response(status=201, headers={
            "Location": url_for("reviewitem", movie=movie, review=movie.reviews.index(review))
        })

class ReviewItem(Resource):
    """Review item resource"""
    def get(self, movie, review):
        try:
            body = ReviewSystemBuilder(movie.reviews[review].serialize())
        except IndexError:
            return Response(status=404)
        body.add_namespace("revsys", LINK_RELATIONS_URL)
        body.add_control_delete_review(movie, review)
        body.add_control("self", url_for("reviewitem",  movie=movie, review=review))
        body.add_control("profile", REVIEW_PROFILE)
        body.add_control("collection", url_for("reviewcollection", movie=movie))
        try:
            return Response(json.dumps(body), 200, mimetype=MASON)
        except:
            return Response(status=404)

    @check_api_key
    def delete(self, movie, review):
        review = movie.reviews[review]
        db.session.delete(review)
        db.session.commit()
        return Response(status=204)


    @check_api_key
    def put(self, movie, review):
        reviewobj = movie.reviews[review]
        api_key = request.headers["API-key"]
        if api_key:
            if reviewobj.user.apikey.key != api_key:
                return Response(status=401)
        else:
            return Response(status=400)
        try:
            requestdict = request.json
        except Exception as e:
            return Response(status=415)
        try:
            validate(requestdict, Review.json_schema())
        except ValidationError as error:
            raise BadRequest(description=str(error)) from error
        try:
            reviewobj.rating = requestdict["rating"]
        except:
            pass
        try:
            reviewobj.comment = requestdict["comment"]
        except:
            pass
        reviewobj.date=datetime.now()
        movie.update_rating()
        db.session.commit()
        return Response(status=204)
