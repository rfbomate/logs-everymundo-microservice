
import requests
import json

BASE_URL = 'https://js33rzfdnl.execute-api.us-east-1.amazonaws.com/dev/'

# test verify to generate notifications


def testVerifyCorrectNotify():
    header = {'content-type': 'application/json'}
    response = requests.post(BASE_URL+'notify',
                             headers=header, data=json.dumps({}))
    responseJson = response.json()

    assert (response.status_code ==
            200 and responseJson['message'] == 'Notifications are sended ok')
