from email import header
import requests
import json

BASE_URL = 'https://js33rzfdnl.execute-api.us-east-1.amazonaws.com/dev/'


# verify that not send input params
def testVerifyIfSendSomeParam():
    header = {'content-type': 'application/json'}
    response = requests.post(BASE_URL+'filterLogs',
                             headers=header, data=json.dumps({}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == 'At least a param must send to filter logs')


# test when exist limit and not offset
def testVerifyExistLimitAbdNotOffset():
    header = {'content-type': 'application/json'}
    response = requests.post(BASE_URL+'filterLogs',
                             headers=header, data=json.dumps({"application": "Iberia", "limit": "10"}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == 'If you pass limit, you must pass offset')


# test verify if limit is an integer value
def testVerifyLimitIsInteger():
    header = {'content-type': 'application/json'}
    response = requests.post(BASE_URL+'filterLogs',
                             headers=header, data=json.dumps({"application": "Iberia", "offset": "0", "limit": 'jarro'}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == 'The limit must be a integer value')


# test verify if we send offset and not limit
def testVerifyOffsetAndNotLimit():
    header = {'content-type': 'application/json'}
    response = requests.post(BASE_URL+'filterLogs',
                             headers=header, data=json.dumps({"application": "Iberia", "offset": "0"}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == 'If you pass offset, you must pass limit')


# test verify offset is integer value
def testVerifyOffsetIsIntegerValue():
    header = {'content-type': 'application/json'}
    response = requests.post(BASE_URL+'filterLogs',
                             headers=header, data=json.dumps({"application": "Iberia", 'limit': 3, "offset": "lolo"}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == 'The offset must be a integer value')


# test verify format begin date
def testVerifyBeginDateFormat():
    header = {'content-type': 'application/json'}
    response = requests.post(BASE_URL+'filterLogs',
                             headers=header, data=json.dumps({"application": "Iberia", 'timestampBegin': '2021-04-12'}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == "Timestamp of begin haven't a correct format YYYY-MM-DDTHH:MM")


# test verify date format with pattern
def testVerifyBeginDateFormatWithPattern():
    header = {'content-type': 'application/json'}
    response = requests.post(BASE_URL+'filterLogs',
                             headers=header, data=json.dumps({"application": "Iberia", 'timestampBegin': '2021-13-12T10:30'}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == "Date format is incorrect in begin timestamp")


# test verify hours format with pattern begin date
def testVerifyBeginDateFormatWithPatternHours():
    header = {'content-type': 'application/json'}
    response = requests.post(BASE_URL+'filterLogs',
                             headers=header, data=json.dumps({"application": "Iberia", 'timestampBegin': '2021-11-12T10:80'}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == "Hours format is incorrect in begin timestamp")


# test verify format end date
def testVerifyEndDateFormat():
    header = {'content-type': 'application/json'}
    response = requests.post(BASE_URL+'filterLogs',
                             headers=header, data=json.dumps({"application": "Iberia", 'timestampEnd': '2021-04-12'}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == "Timestamp of end haven't a correct format YYYY-MM-DDTHH:MM")


# test verify date format with pattern
def testVerifyEndDateFormatWithPattern():
    header = {'content-type': 'application/json'}
    response = requests.post(BASE_URL+'filterLogs',
                             headers=header, data=json.dumps({"application": "Iberia", 'timestampEnd': '2021-13-12T10:30'}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == "Date format is incorrect in end timestamp")


# test verify hours format with pattern end date
def testVerifyEndDateFormatWithPatternHours():
    header = {'content-type': 'application/json'}
    response = requests.post(BASE_URL+'filterLogs',
                             headers=header, data=json.dumps({"application": "Iberia", 'timestampEnd': '2021-11-12T10:80'}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == "Hours format is incorrect in end timestamp")


# test verify end date is greater than begin date
def testVerifyEndDateFormatWithPatternHours():
    header = {'content-type': 'application/json'}
    response = requests.post(BASE_URL+'filterLogs',
                             headers=header, data=json.dumps({"application": "Iberia", 'timestampEnd': '2020-11-11T12:25', 'timestampBegin': '2021-11-12T10:10'}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == "The start date must be less than the End date")


# test verify category is not allowed
def testVerifyCategoryIsNotAllowed():
    header = {'content-type': 'application/json'}
    response = requests.post(BASE_URL+'filterLogs',
                             headers=header, data=json.dumps({"application": "Iberia", 'category': "ERRORES"}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == "The category is not allowed")


# test verify severity error is not allowed
def testVerifySeverityIsNotAllowed():
    header = {'content-type': 'application/json'}
    response = requests.post(BASE_URL+'filterLogs',
                             headers=header, data=json.dumps({"application": "Iberia", 'severity': "6"}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == "The level of severity is not allowed")


# test verify correct search
def testVerifySeverityIsNotAllowed():
    header = {'content-type': 'application/json'}
    response = requests.post(BASE_URL+'filterLogs',
                             headers=header, data=json.dumps({"application": "Iberia"}))
    responseJson = response.json()

    assert (response.status_code ==
            200 and responseJson['message'] == "Search made ok")
