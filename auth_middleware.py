from functools import wraps
import jwt
from flask import request, abort
import os


SECRET_KEY = os.environ['SECRET_KEY']


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            splitedValue = data['emailAndId']
            resultSplit = splitedValue.split('~')
            if(len(resultSplit) != 2):
                return {'message': "Bad format in token"}

            current_user = {'email': resultSplit[0], 'userId': resultSplit[1]}

            if current_user is None:
                return {
                    "message": "Invalid Authentication token!",
                    "data": None,
                    "error": "Unauthorized"
                }, 401

        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return f(current_user, *args, **kwargs)

    return decorated
