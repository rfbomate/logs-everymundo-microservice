import email
from posixpath import split
from flask import jsonify
import os
import boto3
from datetime import datetime


def notifyService(request):
    actualDate = datetime.today().strftime('%Y-%m-%d')
    session = boto3.Session(
        aws_access_key_id=os.environ['ACCESS_KEY'], aws_secret_access_key=os.environ['SECRET_KEY'])
    fileName = actualDate+'.txt'
    s3 = session.resource('s3')
    fileObject = s3.Bucket(os.environ['BUCKET_NAME_SUSCRIPTORS']).Object(
        fileName)  # read a specific file
    if(not fileObject):
        return jsonify({"message": "Can't read the subscribers file in this moment"}), 400

    body = fileObject.get()['Body'].read().decode('utf-8')
    textReaded = str(body)

    listLines = textReaded.split("\n")
    listForMail = []
    for line in listLines:
        separated = line.split('-')
        email = separated[0]
        application = separated[1]
        category = separated[2]

        # ingreso los elementos a la lista para poder envir los respectivos mails

    return jsonify({'message': 'Data saved ok'})
