from flask import Blueprint, request, jsonify, json, make_response, render_template
import jwt
from api.models import User, login_required, AccessLevel
from api import app, bcrypt, mysql
import datetime

authentication = Blueprint('authentication', __name__)

@authentication.route('/', methods = ['GET'])
@login_required
def check_token(current_user):
    return jsonify({'message': f'Token is valid for use {current_user.user_id} with acccess {current_user.access.name}'}), 201

@authentication.route('/login', methods = ['POST'])
def login_user():

    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Login required', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})
    
    #make database query in the user table by the username and their stored password
    #replace the line below with the query results
    user = User(1234, AccessLevel.player)
    if not user:
        return make_response('Username not found', 401, {'WWW-Authenticate' : 'Basic realm="Username not found"'})
    
    #compare stored password with hashed current password instead of True below
    if not True: #bcrypt.check_password_hash(user.password, quere_data.get('password'))
        #if passwords didnt match
        return make_response('Invalid Password', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

        
    #check database password with the stored one
    token = jwt.encode({'user_id' : user.user_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30), 'access' : user.access.value}, app.config['SECRET_KEY'])
    return jsonify({'token' : token.decode('UTF-8')}), 201



@authentication.route('/register', methods = ['POST'])
def register_user():
    user = request.json #now user is a python dict and with keys as string
    print(user['first_name']) #print's the request first_name field. 
    #call db stored procedure
    #process result (handle error)
    #return success/reason for fail
    return 'POST to /register'