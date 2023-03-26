'''User authentication functionality'''
import secrets

from flask import request, Response
from review_system.models import ApiKey

def check_api_key(func):
    '''Check if user has valid API key'''
    def wrapper(*args, **kwargs):
        key = request.headers.get("API-Key")
        if key is not None:
            keys = ApiKey.query.all()
            for db_key in keys:
                if secrets.compare_digest(key, db_key.key):
                    return func(*args, **kwargs)
        return Response(status=401)
    return wrapper
