# app.py


import os
import time
from itsdangerous import exc
import jwt
from auth_middleware import token_required
from datetime import datetime

import boto3
import botocore


from flask import Flask, request, jsonify
app = Flask(__name__)

# environment variables
SECRET_KEY = os.environ['SECRET_KEY']
os.environ['TZ'] = 'America/Guayaquil'


@app.route("/", methods=['GET'])
def hello():
    return {
        "message": "Main page"
    }, 200


@app.route("/createSingleLog", methods=["POST"])
@token_required
def createSingleLog(current_user):

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

    try:
        session = boto3.Session(
            aws_access_key_id=os.environ['ACCESS_KEY'], aws_secret_access_key=os.environ['SECRET'])

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


@app.route('/statsLogsByFile', methods=['POST'])
def statsLogsByFile():
    if('file' not in request.files):
        return jsonify({'message': "No file item founded"}), 400

    fileUploaded = request.files['file']

    if(fileUploaded.filename == ''):
        return jsonify({'message': "Not selected file"}), 400

    if(not _isValidExtension(fileUploaded.filename)):
        return jsonify({'message': "Extension not allowed"}), 400

    # save temporal file
    s3 = boto3.client(
        "s3", aws_access_key_id=os.environ['ACCESS_KEY'], aws_secret_access_key=os.environ['SECRET'])

    try:
        s3.upload_fileobj(
            fileUploaded,
            os.environ['BUCKET_NAME'],
            fileUploaded.filename,
            ExtraArgs={
                "ContentType": fileUploaded.content_type
            }
        )

        # read temporal file
        textReaded = ''
        session = boto3.Session(
            aws_access_key_id=os.environ['ACCESS_KEY'], aws_secret_access_key=os.environ['SECRET'])

        s3 = session.resource('s3')
        fileObjectRead = s3.Bucket(os.environ['BUCKET_NAME']).Object(
            fileUploaded.filename)  # read a specific file
        if(not fileObjectRead):
            return jsonify({"message": "An error has occured reading the file"}), 400

        body = fileObjectRead.get()['Body'].read().decode('utf-8')
        textReaded = str(body)

        # delete temporal file
        fileObjectRead.delete()

        # processing file
        lines = textReaded.split("\n")
        countErrors = 0
        countSuccess = 0
        isValidFile = True
        counterLineError = 0
        for line in lines:
            columns = line.split("-")  # 0-timestamp 1-application 2-category
            if(len(columns) != 3):
                isValidFile = False
                break

            if(len(columns[2].split(":")) < 1):
                isValidFile = False
                break

            category = columns[2].split(":")[0]

            if('ERROR' in category.upper()):
                countErrors += 1
            if('SUCCESS' in category.upper()):
                countSuccess += 1

            counterLineError += 1

        return jsonify({'ErrorCount': countErrors, 'SuccessCount': countSuccess, 'Total': len(lines)}) if isValidFile else jsonify({message: "The file has errors. Error near line "+str(counterLineError+1)}), 400

    except Exception as e:
        return jsonify({"message": "An error has occurred. Retry later"}), 400


def _isValidExtension(pFilename):
    ALLOWED_EXTENSIONS = {'txt'}
    return '.' in pFilename and \
           pFilename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/filterLogs", methods=['POST'])
def filterLogs():
    try:
        # set of allow values for categories and level of error
        typeOfCategory = ['ERROR', 'SUCCESS', 'INFO']  # categories allowed
        typeOfLevel = ['1', '2', '3', '4', '5']  # level error allowed

        timestampBegin = request.json.get('timestampBegin')
        timestampEnd = request.json.get('timestampEnd')
        application = request.json.get('application')
        category = request.json.get('category')
        severity = request.json.get('severity')

        # when both field are empties, not exist pagination process
        limit = request.json.get('limit')
        offset = request.json.get('offset')

        if(not timestampBegin and not timestampEnd and not application and not category and not severity):
            return jsonify({'message': "At least a param must send to filter logs"}), 400

        dateFormat = "%Y-%m-%d"
        hoursFormat = "%H:%M"

        if(timestampBegin):
            separatedTimestampBegin = timestampBegin.split("T")
            if(len(separatedTimestampBegin) != 2):
                return jsonify({'message': "Timestamp of begin haven't a correct format YYYY-MM-DDTHH:MM"}), 400

            try:
                datetime.strptime(separatedTimestampBegin[0], dateFormat)
            except Exception as exceptionFormatDate:
                return jsonify({'message': "Date format is incorrect in begin timestamp"}), 400

            try:
                datetime.strptime(separatedTimestampBegin[1], hoursFormat)
            except Exception as exceptionFormatHours:
                return jsonify({'message': "Hours format is incorrect in begin timestamp"}), 400

        if(timestampEnd):
            separatedTimestampEnd = timestampEnd.split("T")
            if(len(separatedTimestampEnd) != 2):
                return jsonify({'message': "Timestamp of end haven't a correct format YYYY-MM-DDTHH:MM"}), 400

            try:
                datetime.strptime(separatedTimestampEnd[0], dateFormat)
            except Exception as exceptionFormatDate:
                return jsonify({'message': "Date format is incorrect in end timestamp"}), 400

            try:
                datetime.strptime(separatedTimestampEnd[1], hoursFormat)
            except Exception as exceptionFormatHours:
                return jsonify({'message': "Hours format is incorrect in end timestamp"}), 400

        if(timestampBegin and timestampEnd):
            if(timestampBegin >= timestampEnd):
                return jsonify({"message": "The start date must be less than the End date"}), 400

        if(category and not (category in typeOfCategory)):
            return jsonify({"message": "The category is not allowed"})

        if(severity and not(severity in typeOfLevel)):
            return jsonify({"message": "The level of severity is not allowed"})

        logsFiles = []
        session = boto3.Session(
            aws_access_key_id=os.environ['ACCESS_KEY'], aws_secret_access_key=os.environ['SECRET'])
        s3 = session.resource('s3')
        bucketObject = s3.Bucket(os.environ['BUCKET_NAME'])
        for my_bucket_object in bucketObject.objects.all():
            key = my_bucket_object.key
            separatedKey = key.split('.')[0]
            separatedDateKey = separatedKey.split('-')
            # selected files for search
            if(timestampBegin and not timestampEnd):
                separatedTimestampBegin = timestampBegin.split("T")
                separatedDateBegin = separatedTimestampBegin[0].split("-")
                if(str(separatedDateKey[0]) >= str(separatedDateBegin[0])):
                    logsFiles.append(my_bucket_object)

            if(not timestampBegin and timestampEnd):
                separatedTimestampEnd = timestampEnd.split("T")
                separatedDateEnd = separatedTimestampEnd[0].split("-")
                if(str(separatedDateKey[0]) <= str(separatedDateEnd[0])):
                    logsFiles.append(my_bucket_object)

            if(timestampBegin and timestampEnd):
                separatedTimestampBegin = timestampBegin.split("T")
                separatedDateBegin = separatedTimestampBegin[0].split("-")

                separatedTimestampEnd = timestampEnd.split("T")
                separatedDateEnd = separatedTimestampEnd[0].split("-")

                if(str(separatedDateKey[0]) >= str(separatedDateBegin[0]) and str(separatedDateKey[0]) <= str(separatedDateEnd[0])):
                    logsFiles.append(my_bucket_object)

        # load entry logs of the selected files
        entryLogs = []
        for itemFile in logsFiles:
            fileObjectRead = s3.Bucket(os.environ['BUCKET_NAME']).Object(
                itemFile.key)  # read a specific file
            if(not fileObjectRead):
                return jsonify({"message": "An error has occured reading the file"}), 400

            body = fileObjectRead.get()['Body'].read().decode('utf-8')
            textReaded = str(body)

            entryLogs += textReaded.split("\n")

        # we begin to scan de logs
        for itemLog in entryLogs:
            logParts = itemLog.split('-')
            # we validate the format because the could be corrupt for third people
            # if itemLog is corrupted, this item don't show in the list

            timestampCursor = logParts[0]
            applicationCursor = logParts[1]
            categoryCursor = logParts[2]

        return jsonify({"result": len(entryLogs)})

    except Exception as e:
        return jsonify({'message': str(e)}), 400


@app.route("/getToken", methods=['POST'])
def getToken():
    email = request.json.get('email')
    userId = request.json.get('userId')

    if(not email or not userId):
        return jsonify({'message': "The input params does not complete"})

    token = jwt.encode({'emailAndId': email+'~'+userId}, SECRET_KEY)

    return jsonify({'token': token})
