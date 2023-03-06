from flask import request, Response
from review_system.models import ApiKey

def check_api_key(func):
    def wrapper(*args, **kwargs):
        keys = ApiKey.query.all()
        json_keys = []
        for key in keys:
            json_keys.append(key.Serialize()["key"])
        if request.headers.get('API-Key') in json_keys:
            return func(*args, **kwargs)
        return Response(status=401)
    return wrapper
