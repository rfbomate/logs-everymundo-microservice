from flask import jsonify
import os
import jwt
SECRET_KEY = os.environ['SECRET_KEY']


def getTokenService(request):
    email = request.json.get('email')
    userId = request.json.get('userId')

    if(not email or not userId):
        return jsonify({'message': "The input params does not complete"})

    token = jwt.encode({'emailAndId': email+'~'+userId}, SECRET_KEY)

    return jsonify({'token': token})
