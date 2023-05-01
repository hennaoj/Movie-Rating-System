"""User resource module"""
import json
import secrets
from datetime import datetime
from jsonschema import validate, ValidationError
from flask import Response, request, url_for
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from review_system import db
from review_system.models import User, Apikey
from review_system.auth import check_api_key
from review_system.constants import *
from review_system.utils import ReviewSystemBuilder


class UserCollection(Resource):
    """User collection resource"""
    def post(self):
        if not request.json:
            return Response(status=415)
        try:
            validate(request.json, User.json_schema())
        except ValidationError as error:
            print(error)
            raise BadRequest(description=str(error)) from error

        user = User(
            username=request.json["username"],
            age=request.json["age"],
            account_creation_date=datetime.now(),
            gender=request.json["gender"],
        )
        db.session.add(user)
        db.session.commit()

        for i in range(10):
            try:
                token = secrets.token_hex(32)
                db_key = Apikey(key = token)
                db.session.add(db_key)
                user.apikey = db_key
                db.session.commit()
                break
            except Exception as e:
                print(e)
                pass
            return Response(status=404)
        return Response(status=201, headers={"API-key": db_key.key})
