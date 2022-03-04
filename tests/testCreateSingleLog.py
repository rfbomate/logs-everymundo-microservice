
import requests
import json

BASE_URL = 'https://js33rzfdnl.execute-api.us-east-1.amazonaws.com/dev/'

# verify if the request without token fail


def testVerifyNotAllowedWithoutToken():
    response = requests.post(BASE_URL+'createSingleLog', data={})
    assert response.status_code == 401


# verify if we send application params
def testVerifyNotSendApplicationParams():
    headers = {
        'content-type': 'application/json',
    }
    params = (
        ('priority', 'normal'),
    )
    response = requests.post(
        BASE_URL+'getToken',
        headers=headers,
        params=params,
        data=json.dumps({"email": "rfbomate86@gmail.com",
                        "userId": "user-2347474"})
    ).json()

    token = response['token']

    headersAuth = {'Authorization': 'Bearer ' +
                   str(token), 'content-type': 'application/json'}
    response = requests.post(BASE_URL+'createSingleLog',
                             headers=headersAuth, data=json.dumps({}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == 'The application param is required')


# verify if we send the application param like a string value
def testVerifyApplicationParamsIsString():
    headers = {
        'content-type': 'application/json',
    }
    params = (
        ('priority', 'normal'),
    )
    response = requests.post(
        BASE_URL+'getToken',
        headers=headers,
        params=params,
        data=json.dumps({"email": "rfbomate86@gmail.com",
                        "userId": "user-2347474"})
    ).json()

    token = response['token']

    headersAuth = {'Authorization': 'Bearer ' +
                   str(token), 'content-type': 'application/json'}
    response = requests.post(BASE_URL+'createSingleLog',
                             headers=headersAuth, data=json.dumps({"application": 5}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == 'The application param must be a string value')


# verify if we send the category param
def testVerifyCategoryParams():
    headers = {
        'content-type': 'application/json',
    }
    params = (
        ('priority', 'normal'),
    )
    response = requests.post(
        BASE_URL+'getToken',
        headers=headers,
        params=params,
        data=json.dumps({"email": "rfbomate86@gmail.com",
                        "userId": "user-2347474"})
    ).json()

    token = response['token']

    headersAuth = {'Authorization': 'Bearer ' +
                   str(token), 'content-type': 'application/json'}
    response = requests.post(BASE_URL+'createSingleLog',
                             headers=headersAuth, data=json.dumps({"application": "Iberia"}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == 'The category param is required')

# verify if we send the category param like a string value


def testVerifyCategoryParamsIsString():
    headers = {
        'content-type': 'application/json',
    }
    params = (
        ('priority', 'normal'),
    )
    response = requests.post(
        BASE_URL+'getToken',
        headers=headers,
        params=params,
        data=json.dumps({"email": "rfbomate86@gmail.com",
                        "userId": "user-2347474"})
    ).json()

    token = response['token']

    headersAuth = {'Authorization': 'Bearer ' +
                   str(token), 'content-type': 'application/json'}
    response = requests.post(BASE_URL+'createSingleLog',
                             headers=headersAuth, data=json.dumps({"application": "Iberia", "category": 5}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == 'The category param must be a string value')


# verify if we send the description param
def testVerifyDescriptionParams():
    headers = {
        'content-type': 'application/json',
    }
    params = (
        ('priority', 'normal'),
    )
    response = requests.post(
        BASE_URL+'getToken',
        headers=headers,
        params=params,
        data=json.dumps({"email": "rfbomate86@gmail.com",
                        "userId": "user-2347474"})
    ).json()

    token = response['token']

    headersAuth = {'Authorization': 'Bearer ' +
                   str(token), 'content-type': 'application/json'}
    response = requests.post(BASE_URL+'createSingleLog',
                             headers=headersAuth, data=json.dumps({"application": "Iberia", "category": "ERROR"}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == 'The description param is required')


# verify if description param is string
def testVerifyDescriptionParamsIsString():
    headers = {
        'content-type': 'application/json',
    }
    params = (
        ('priority', 'normal'),
    )
    response = requests.post(
        BASE_URL+'getToken',
        headers=headers,
        params=params,
        data=json.dumps({"email": "rfbomate86@gmail.com",
                        "userId": "user-2347474"})
    ).json()

    token = response['token']

    headersAuth = {'Authorization': 'Bearer ' +
                   str(token), 'content-type': 'application/json'}
    response = requests.post(BASE_URL+'createSingleLog',
                             headers=headersAuth, data=json.dumps({"application": "Iberia", "category": "ERROR", "description": 44}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == 'The description param must be a string value')

# verify if category is allowed


def testVerifyCategoryIsAllowed():
    headers = {
        'content-type': 'application/json',
    }
    params = (
        ('priority', 'normal'),
    )
    response = requests.post(
        BASE_URL+'getToken',
        headers=headers,
        params=params,
        data=json.dumps({"email": "rfbomate86@gmail.com",
                        "userId": "user-2347474"})
    ).json()

    token = response['token']

    headersAuth = {'Authorization': 'Bearer ' +
                   str(token), 'content-type': 'application/json'}
    response = requests.post(BASE_URL+'createSingleLog',
                             headers=headersAuth, data=json.dumps({"application": "Iberia", "category": "ERRORES", "description": "Problema con la consulta"}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == 'The category of log is not allow')


# test link between ERROR categoriy and error level
def testVerifyLinkBetweenErrorAndLevel():
    headers = {
        'content-type': 'application/json',
    }
    params = (
        ('priority', 'normal'),
    )
    response = requests.post(
        BASE_URL+'getToken',
        headers=headers,
        params=params,
        data=json.dumps({"email": "rfbomate86@gmail.com",
                        "userId": "user-2347474"})
    ).json()

    token = response['token']

    headersAuth = {'Authorization': 'Bearer ' +
                   str(token), 'content-type': 'application/json'}
    response = requests.post(BASE_URL+'createSingleLog',
                             headers=headersAuth, data=json.dumps({"application": "Iberia", "category": "ERROR", "description": "Problema con la consulta"}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == 'When is a log of type ERROR, is mandatory to send like param the LEVEL ERROR')


# test if level error is an allowed value
def testVerifyRangeErrorLevel():
    headers = {
        'content-type': 'application/json',
    }
    params = (
        ('priority', 'normal'),
    )
    response = requests.post(
        BASE_URL+'getToken',
        headers=headers,
        params=params,
        data=json.dumps({"email": "rfbomate86@gmail.com",
                        "userId": "user-2347474"})
    ).json()

    token = response['token']

    headersAuth = {'Authorization': 'Bearer ' +
                   str(token), 'content-type': 'application/json'}
    response = requests.post(BASE_URL+'createSingleLog',
                             headers=headersAuth, data=json.dumps({"application": "Iberia", "category": "ERROR", "description": "Problema con la consulta", 'levelError': '7'}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == 'The level of error of the log is not allow')


# test if all values not contain not allowed character
# test if level error is an allowed value
def testVerifyAlloweCharacters():
    headers = {
        'content-type': 'application/json',
    }
    params = (
        ('priority', 'normal'),
    )
    response = requests.post(
        BASE_URL+'getToken',
        headers=headers,
        params=params,
        data=json.dumps({"email": "rfbomate86@gmail.com",
                        "userId": "user-2347474"})
    ).json()

    token = response['token']

    headersAuth = {'Authorization': 'Bearer ' +
                   str(token), 'content-type': 'application/json'}
    response = requests.post(BASE_URL+'createSingleLog',
                             headers=headersAuth, data=json.dumps({"application": "Iberia", "category": "ERROR", "description": "Problema con - la consulta", 'levelError': '4'}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == "Symbols : and - are reserved words of the syntaxis of the log input. You can't use them")


# verify correct process
def testVerifyCorrectProcess():
    headers = {
        'content-type': 'application/json',
    }
    params = (
        ('priority', 'normal'),
    )
    response = requests.post(
        BASE_URL+'getToken',
        headers=headers,
        params=params,
        data=json.dumps({"email": "rfbomate86@gmail.com",
                        "userId": "user-2347474"})
    ).json()

    token = response['token']

    headersAuth = {'Authorization': 'Bearer ' +
                   str(token), 'content-type': 'application/json'}
    response = requests.post(BASE_URL+'createSingleLog',
                             headers=headersAuth, data=json.dumps({"application": "Iberia", "category": "SUCCESS", "description": "Query is correct"}))
    responseJson = response.json()

    assert (response.status_code ==
            200 and responseJson['message'] == "Data saved ok")
