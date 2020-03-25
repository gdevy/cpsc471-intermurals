#put classes shared by  some of the API groups here
import datetime as dt
import jwt
from api import app


class TokenManager():
    token_period = dt.timedelta(hours = 5)

    @classmethod
    def create_token(cls, user_id):
        
        newJWT = {
            'exp': dt.datetime.now() + cls.token_period,
            'iat': dt.datetime.now(),
            'user': user_id
        }

        return jwt.encode(newJWT, app.config.get('SECRET_KEY'), algorithm='HS256')

    @staticmethod
    def verify_token(token):
        return 'Invalid token. Login Again', False


class User():

    #variable about db structure

    def __init__(self):
        #constructor
        1 + 1