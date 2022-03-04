from flask import jsonify
import boto3
import time
import os
import botocore


def createSingleLogService(request):

    # set of allow values for categories and level of error
    typeOfCategory = ['ERROR', 'SUCCESS', 'INFO']  # categories allowe
    typeOfLevel = ['1', '2', '3', '4', '5']  # level error allowed

    application = request.json.get('application')
    category = request.json.get('category')
    levelError = request.json.get('levelError')
    description = request.json.get('description')

    # validation input data
    if(not application):
        return jsonify({'message': 'The application param is required'}), 400

    if(not isinstance(application, str)):
        return jsonify({'message': "The application param must be a string value"}), 400

    if(not category):
        return jsonify({'message': 'The category param is required'}), 400

    if(not isinstance(category, str)):
        return jsonify({'message': "The category param must be a string value"}), 400

    if(not description):
        return jsonify({'message': "The description param is required"})

    if(not isinstance(description, str)):
        return jsonify({'message': "The description param must be a string value"}), 400

    if(not (category in typeOfCategory)):
        return jsonify({'message': "The category of log is not allow"}), 400

    if(category == 'ERROR'):
        if(not levelError):
            return jsonify({'message': "When is a log of type ERROR, is mandatory to send like param the LEVEL ERROR"}), 400

        if(not str(levelError) in typeOfLevel):
            return jsonify({'message': "The level of error of the log is not allow"}), 400

    if(('-' in application or ':' in application) or (('-' in category) or (':' in category)) or (('-' in description) or (':' in description))):
        return jsonify({'message': "Symbols : and - are reserved words of the syntaxis of the log input. You can't use them"}), 400
    try:
        session = boto3.Session(
            aws_access_key_id=os.environ['ACCESS_KEY'], aws_secret_access_key=os.environ['SECRET_KEY'])

        s3 = session.resource('s3')
        time.tzset()

        # i create the log text  <timestamp>-<application>-<category>[level]:description
        txt_data = str(time.strftime("%Y%m%dT%H:%M")) + \
            "-" + str(application)+"-"+str(category)
        if(category == 'ERROR'):
            txt_data += '['+str(levelError)+']'
        txt_data += ':'+str(description)

        fileName = str(time.strftime("%Y-%m-%d"))+'.txt'

        try:
            s3.Object(os.environ['BUCKET_NAME'], fileName).load()
        except botocore.exceptions.ClientError as exceptionExist:
            if exceptionExist.response['Error']['Code'] == "404":
                # file not exist and I need create it
                s3Object = s3.Object(os.environ['BUCKET_NAME'], fileName)
                s3Object.put(Body=txt_data)
                return jsonify({'message': 'Data saved ok'})
            else:
                return jsonify({"message": "Something has occurred !!!", "detail": str(exceptionExist)}), 400

        # the file exist, i need insert in the first position the new log

        textReaded = ''

        fileObject = s3.Bucket(os.environ['BUCKET_NAME']).Object(
            fileName)  # read a specific file
        if(not fileObject):
            return jsonify({"message": "The log can't save in this moment. Problem when we try to read the logs file"})

        body = fileObject.get()['Body'].read().decode('utf-8')
        textReaded += str(body)

        # the logs has saved with desc sort
        textReaded = txt_data+'\n'+textReaded

        # save data in s3
        s3Object = s3.Object(os.environ['BUCKET_NAME'], fileName)
        s3Object.put(Body=textReaded)
        return jsonify({'message': 'Data saved ok'})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
