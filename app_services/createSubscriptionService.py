from flask import jsonify
import os

import boto3
import botocore


def createSubscriptionService(request):
    typeOfCategory = ['ERROR', 'SUCCESS', 'INFO']  # categories allowed

    email = request.json.get('email')
    application = request.json.get('application')
    category = request.json.get('category')

    if(not email):
        return jsonify({'message': 'The email is required'}), 400

    if(not application):
        return jsonify({'message': 'The application is required'}), 400

    if(not category):
        return jsonify({'message': 'The category is required'})

    if(category.upper() not in typeOfCategory):
        return jsonify({'message': 'The category is not allowed'}), 400

    if(('-' in email) or ('-' in application) or ('-' in category)):
        return jsonify({'message': "Symbol - is reserved words of the syntaxis of the subscription register. You can't use it"})

    try:
        session = boto3.Session(
            aws_access_key_id=os.environ['ACCESS_KEY'], aws_secret_access_key=os.environ['SECRET_KEY'])

        s3 = session.resource('s3')
        txt_data = email+'-'+application+'-'+category

        fileName = 'suscriptors.txt'

        try:
            s3.Object(os.environ['BUCKET_NAME_SUSCRIPTORS'], fileName).load()
        except botocore.exceptions.ClientError as exceptionExist:
            if exceptionExist.response['Error']['Code'] == "404":
                # file not exist and I need create it
                s3Object = s3.Object(
                    os.environ['BUCKET_NAME_SUSCRIPTORS'], fileName)
                s3Object.put(Body=txt_data)
                return jsonify({'message': 'Data saved ok'})
            else:
                return jsonify({"message": "Something has occurred !!!", "detail": str(exceptionExist)}), 400

        textReaded = ''

        fileObject = s3.Bucket(os.environ['BUCKET_NAME_SUSCRIPTORS']).Object(
            fileName)  # read a specific file
        if(not fileObject):
            return jsonify({"message": "The log can't save in this moment. Problem when we try to read the logs file"}), 400

        body = fileObject.get()['Body'].read().decode('utf-8')
        textReaded += str(body)

        if(verifyDuplicate(email, application, category, textReaded)):
            return jsonify({"message": "The tuple already has been register previusly"}), 400

        # the logs has saved with desc sort
        textReaded = textReaded+'\n'+txt_data

        # save data in s3
        s3Object = s3.Object(os.environ['BUCKET_NAME_SUSCRIPTORS'], fileName)
        s3Object.put(Body=textReaded)
        return jsonify({'message': 'Data saved ok'})

    except Exception as e:
        return jsonify({'message': str(e)}), 400


def verifyDuplicate(email, application, category, textSearch):
    listSubscribers = textSearch.split("\n")
    founded = False
    for itemS in listSubscribers:
        if(itemS == email+'-'+application+'-'+category):
            founded = True
            break

    return founded
