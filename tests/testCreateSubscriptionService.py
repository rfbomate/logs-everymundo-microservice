
from email import header
import requests
import json

BASE_URL = 'https://js33rzfdnl.execute-api.us-east-1.amazonaws.com/dev/'


# verify if we send email param
def testVerifyNotSendEmailParams():
    header = {'content-type': 'application/json'}
    response = requests.post(BASE_URL+'createSubscription',
                             headers=header, data=json.dumps({}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == 'The email is required')


# verify if we send application param
def testVerifyNotSendApplicationParams():
    header = {'content-type': 'application/json'}
    response = requests.post(BASE_URL+'createSubscription',
                             headers=header, data=json.dumps({'email': 'rfbomate86@gmail.com'}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == 'The application is required')


# verify if we send category param
def testVerifyNotSendCategoryParams():
    header = {'content-type': 'application/json'}
    response = requests.post(BASE_URL+'createSubscription',
                             headers=header, data=json.dumps({'email': 'rfbomate86@gmail.com', 'application': 'Iberia'}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == 'The category is required')


# verify if we send a allowed category
def testVerifyCategoryIsNotAllowed():
    header = {'content-type': 'application/json'}
    response = requests.post(BASE_URL+'createSubscription',
                             headers=header, data=json.dumps({'email': 'rfbomate86@gmail.com', 'application': 'Iberia', 'category': 'ERRORES'}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == 'The category is not allowed')


# verify if the input has not invalid character
def testVerifyInputHasInvalidCharacter():
    header = {'content-type': 'application/json'}
    response = requests.post(BASE_URL+'createSubscription',
                             headers=header, data=json.dumps({'email': 'rfbomate86-@gmail.com', 'application': 'Iberia', 'category': 'ERROR'}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == "Symbol is not valid")


# test duplicate register
def testVerifyDuplicateRegister():
    header = {'content-type': 'application/json'}
    response = requests.post(BASE_URL+'createSubscription',
                             headers=header, data=json.dumps({'email': 'rfbomate86@gmail.com', 'application': 'Iberia', 'category': 'ERROR'}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == "The tuple already has been register previusly")


# test create a correct register
def testProcessOk():
    header = {'content-type': 'application/json'}
    response = requests.post(BASE_URL+'createSubscription',
                             headers=header, data=json.dumps({'email': 'rfbomate86@gmail.com', 'application': 'MONCAVE', 'category': 'SUCCESS'}))
    responseJson = response.json()

    assert (response.status_code ==
            200 and responseJson['message'] == "Data saved ok")
