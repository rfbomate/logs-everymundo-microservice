
from flask import jsonify
import os
import boto3
from datetime import datetime
import botocore


def notifyService(request):
    try:
        typeOfCategory = ['ERROR', 'SUCCESS', 'INFO']  # categories allowed

        actualDate = datetime.today().strftime('%Y-%m-%d')
        session = boto3.Session(
            aws_access_key_id=os.environ['ACCESS_KEY'], aws_secret_access_key=os.environ['SECRET_KEY'])

        fileName = 'suscriptors.txt'
        s3 = session.resource('s3')
        fileObject = s3.Bucket(os.environ['BUCKET_NAME_SUSCRIPTORS']).Object(
            fileName)  # read a specific file

        if(not fileObject):
            return jsonify({"message": "Can't read the subscribers file in this moment"}), 400

        body = fileObject.get()['Body'].read().decode('utf-8')

        textReaded = str(body)

        listLines = textReaded.split("\n")

        mailsToSend = {}

        for line in listLines:
            separatedItem = line.split("-")

            email = separatedItem[0]
            application = separatedItem[1]
            category = separatedItem[2]

            if(category.upper() not in typeOfCategory):
                continue

            if(email in mailsToSend.keys()):
                mailsToSend[email].append(
                    {'application': application, 'category': category, 'logs': []})
            else:
                mailsToSend[email] = [{'application': application,
                                       'category': category, 'logs': []}]

        # load logs file
        fileName = actualDate+'.txt'
        # we verify if the logs file is created
        try:
            s3.Object(os.environ['BUCKET_NAME'], fileName).load()
        except botocore.exceptions.ClientError as exceptionExist:
            if exceptionExist.response['Error']['Code'] == "404":
                return jsonify({'message': 'Not exist logs for this date'}), 400
            else:
                return jsonify({"message": "Something has occurred !!!", "detail": str(exceptionExist)}), 400

        s3 = session.resource('s3')
        fileObject = s3.Bucket(os.environ['BUCKET_NAME']).Object(
            fileName)  # read a specific file

        if(not fileObject):
            return jsonify({"message": "Can't read the subscribers file in this moment"}), 400

        body = fileObject.get()['Body'].read().decode('utf-8')

        textReaded = str(body)

        listLines = textReaded.split("\n")

        # fill logs input by user and conditions
        for itemLog in listLines:
            separatedLog = itemLog.split("-")
            if(len(separatedLog) != 3):
                continue

            applicationLog = separatedLog[1]
            category = separatedLog[2]

            separatedCategory = category.split(":")
            if(len(separatedCategory) != 2):
                continue

            areacategory = separatedCategory[0]
            if('ERROR' in areacategory):
                categoryItemLog = areacategory[0:areacategory.index(
                    '[')]
            else:
                categoryItemLog = areacategory

            newListMails = {}
            for key in mailsToSend.keys():
                listSuscriptions = mailsToSend[key]
                for itemSuscription in listSuscriptions:
                    if(itemSuscription['application'].upper() == applicationLog.upper() and itemSuscription['category'].upper() == categoryItemLog.upper()):
                        if(key in newListMails.keys()):
                            newListMails[key] = newListMails[key] + [itemLog]
                        else:
                            newListMails[key] = [itemLog]

            # send mails
            for itemKey in newListMails.keys():
                logsAsString = ''
                listLogs = newListMails[itemKey]

                for itemListBug in listLogs:
                    logsAsString += str(itemListBug)+'\n'

                message = 'Hi '+str(itemKey)+'\n' + \
                    '<h1>List of logs</h1>'+'\n'+logsAsString

                notify(str(itemKey), message)

        return jsonify({'message': 'Notifications are sended ok'})
    except Exception as e:
        return jsonify({"message": str(e)})

# mock function that simulate the send email


def notify(email, content):
    return {"email": email, "content": content}
