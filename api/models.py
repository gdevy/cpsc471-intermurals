#put classes shared by  some of the API groups here
import datetime
from enum import Enum
import jwt
from flask import request, jsonify, make_response
from api import app
from functools import wraps

class AccessLevel(Enum):
        admin = 1
        referee = 2
        player = 3

class User:
    
    def __init__(self, user_id, access):
        self.access = access
        self.user_id = user_id
        self.password = None


def login_required(func):

    @wraps(func)
    def wrapper_decorator(*args, **kwargs):
        token = request.headers.get("Authorization")
        if token:
            token = token.split(" ")[1]
            try:
                payload = jwt.decode(token, app.config['SECRET_KEY'])
            except jwt.ExpiredSignatureError:
                print('invalid time signature')
                return make_response('Time expired, please log in again', 401, {'WWW-Authenticate' : 'Basic realm="Username not found"'})
            except jwt.InvalidTokenError:
                print('invalid token')
                return make_response('Token signed imporperly', 401, {'WWW-Authenticate' : 'Basic realm="Username not found"'})
        
        current_user = User(payload['user_id'], AccessLevel(payload['access']))
        return func(current_user, *args, **kwargs)
        
    return wrapper_decorator

