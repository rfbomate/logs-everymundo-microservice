from flask import jsonify
import boto3
import os
from datetime import datetime


def filterLogsServices(request):
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
        limit = str(request.json.get('limit'))
        offset = str(request.json.get('offset'))

        if(not timestampBegin and not timestampEnd and not application and not category and not severity):
            return jsonify({'message': "At least a param must send to filter logs"}), 400

        if(limit):
            if(not offset):
                return jsonify({'message': "If you pass limit, you must pass offset"}), 400

            if(not isinstance(int(limit), int)):
                return jsonify({'message': 'The limit must be a integer value'}), 400

        if(offset):
            if not limit:
                return jsonify({'message': "If you pass offset, you must pass limit"}), 400

            if(not isinstance(int(offset), int)):
                return jsonify({'message': 'The offset must be a integer value'}), 400

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
            aws_access_key_id=os.environ['ACCESS_KEY'], aws_secret_access_key=os.environ['SECRET_KEY'])
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

            if(not timestampBegin and not timestampEnd):
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

        result = []
        # we begin to scan de logs
        for itemLog in entryLogs:
            logParts = itemLog.split('-')
            # we validate the format because the could be corrupt for third people
            # if itemLog is corrupted, this item don't show in the list

            timestampCursor = logParts[0]
            applicationCursor = logParts[1]
            categoryCursorFull = logParts[2]

            try:
                dateTimeFormat = "%Y%m%dT%H:%M"
                datetime.strptime(timestampCursor, dateTimeFormat)
            except Exception as exceptionFormatDate:
                continue

            categoryCursor = categoryCursorFull.split(":")
            if(len(categoryCursor) != 2):
                continue

            categoryCursor = categoryCursor[0]
            if 'ERROR' in categoryCursor:
                categoryCursor = categoryCursor[0:categoryCursor.index(
                    '[')]

            if(not (categoryCursor in typeOfCategory)):
                continue

            # init condition to compare
            conditionApplication = True
            conditionCategory = True
            conditionSeverity = True
            conditionTimestamp = True
            timestampBegin = timestampBegin.replace("-", "")
            timestampEnd = timestampEnd.replace("-", "")

            if(timestampBegin and not timestampEnd):
                if(timestampCursor < timestampBegin):
                    conditionTimestamp = False

            if(not timestampBegin and timestampEnd):
                if(timestampCursor > timestampEnd):
                    conditionTimestamp = False

            if(timestampBegin and timestampEnd):
                if((timestampCursor < timestampBegin) or (timestampCursor > timestampEnd)):
                    conditionTimestamp = False

            if(application):
                if(application.upper() not in applicationCursor.upper()):
                    conditionApplication = False

            if category or severity:
                categorySplit = categoryCursorFull.split(":")

                if(len(categorySplit) != 2):
                    continue

                categoryAndSeverity = categorySplit[0]

                # if exist severity, the category has to be ERROR
                if(severity):
                    if 'ERROR' not in categoryAndSeverity:
                        continue

                if 'ERROR' in categoryAndSeverity:
                    severityItem = categoryAndSeverity[-2]
                    categoryItem = categoryAndSeverity[0:categoryAndSeverity.index(
                        '[')]
                else:
                    categoryItem = categoryAndSeverity

                if(category):
                    if(category.upper() != categoryItem.upper()):
                        conditionCategory = False

                if(severity):
                    if(severityItem != severity):
                        conditionSeverity = False

            if(conditionApplication and conditionCategory and conditionSeverity and conditionTimestamp):
                result.append(itemLog)

        if(not limit and not offset):
            return jsonify({"result": result})

        # we begin with the pagination process
        limit = int(limit)
        offset = int(offset)

        # borders of results
        inicio = offset*limit
        fin = inicio + limit

        segment = result[inicio:fin]
        totalElements = len(result)
        if totalElements == 0:
            totalPages = 0
        else:
            totalPages = int(
                totalElements / limit) if totalElements % limit == 0 else int(totalElements // limit)+1
        return jsonify({'result': segment, 'totalElements': totalElements, 'totalPages': totalPages, 'offset': offset, 'limit': limit})
    except Exception as e:
        return jsonify({'message': str(e)}), 400
