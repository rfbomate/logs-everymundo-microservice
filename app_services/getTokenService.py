from flask import jsonify
import os
import jwt
SECRET_KEY = os.environ['SECRET_KEY']


def getTokenService(request):
    try:
        email = request.json.get('email')
        userId = request.json.get('userId')
    except Exception as e:
        return jsonify({'message': 'The input is not complete', "description": str(e)}), 400

    if(not email or not userId):
        return jsonify({'message': "The input is not complete"}), 400

    token = jwt.encode({'emailAndId': email+'~'+userId}, SECRET_KEY)

    return jsonify({'token': token, 'message': 'Data saved ok'})
