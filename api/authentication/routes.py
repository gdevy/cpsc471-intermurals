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
        return make_response('Login Information Incomplete', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})
    
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('get_password', [auth.username])
    data = cursor.fetchall()

    if (len(data) != 1) or (data[0][0] != auth.password):
        return make_response('Inalid Credentials', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

    user = User(data[0][1], AccessLevel.referee)  #change to User(data[0][1], data[0][2]) when user type flag is aded

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