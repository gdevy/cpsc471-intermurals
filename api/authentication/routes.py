from flask import Blueprint, request, jsonify, json
from api.models import TokenManager

authentication = Blueprint('authentication', __name__)

@authentication.route('/', methods = ['POST'])
def check_token():
    user, status = TokenManager.verify_token(request.headers['auth_token'])
    if not status:
        return 'Bad Token', 501
    else:
        return user, 200
    

@authentication.route('/register', methods = ['POST'])
def register_user():
    user = request.json #now user is a python dict and with keys as string
    print(user['first_name']) #print's the request first_name field. 
    #call db stored procedure
    #process result (handle error)
    #return success/reason for fail
    return 'POST to /register'