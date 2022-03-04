
import requests
import json

BASE_URL = 'https://js33rzfdnl.execute-api.us-east-1.amazonaws.com/dev/'


# verify error input param
def testVerifyIfSendSomeParam():
    header = {'content-type': 'application/json'}
    response = requests.post(BASE_URL+'getToken',
                             headers=header, data=json.dumps({}))
    responseJson = response.json()

    assert (response.status_code ==
            400 and responseJson['message'] == 'The input is not complete')


# verify generate token ok
def testVerifCorrectTokenGenerated():
    header = {'content-type': 'application/json'}
    response = requests.post(BASE_URL+'getToken',
                             headers=header, data=json.dumps({"email": "rfbomate86@gmail.com", "userId": "user-1233"}))
    assert response.status_code == 200
