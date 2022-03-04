# app.py


from crypt import methods
import os

from auth_middleware import token_required


# import services behavior
from app_services.createSingleLogService import createSingleLogService
from app_services.statsLogsByFileService import statsLogsByFileService
from app_services.filterLogsServices import filterLogsServices
from app_services.getTokenService import getTokenService
from app_services.createSubscriptionService import createSubscriptionService
from app_services.notifyService import notifyService


from flask import Flask, request, jsonify
app = Flask(__name__)

# environment variables
os.environ['TZ'] = 'America/Guayaquil'


@app.route("/createSingleLog", methods=["POST"])
@token_required
def createSingleLog(current_user):
    return createSingleLogService(request)


@app.route('/statsLogsByFile', methods=['POST'])
def statsLogsByFile():
    return statsLogsByFileService(request)


@app.route("/filterLogs", methods=['POST'])
def filterLogs():
    return filterLogsServices(request)


@app.route("/createSubscription", methods=['POST'])
def createSubscription():
    return createSubscriptionService(request)


@app.route("/notify", methods=["POST"])
def notify():
    return notifyService(request)


@app.route("/getToken", methods=['POST'])
def getToken():
    return getTokenService(request)
