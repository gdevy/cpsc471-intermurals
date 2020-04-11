from flask import Blueprint, jsonify, request
from api.models import login_required, User, AccessLevel
from api import mysql
import pymysql

schedule = Blueprint('schedule', __name__)


@schedule.route('/game/', methods = ['PUT'])
@login_required
def record_game(current_user):
    req = request.json
    print(req)

    if current_user.access is not AccessLevel.referee:
        return jsonify({'message' : 'Invalid access level, needs a referee'}), 401
    
    if False: #made a db query to see if ref for game_id matches the current ref
        return jsonify({'message' : 'The results can only be posted by a game referee'}), 401
    
    #call stored procedure for storing the game result
    return jsonify({'message' : 'Needs the Stored Procedure implemented'}), 501


@schedule.route('/referee/', methods = ['POST'])
@login_required
def post_ref_schedule(current_user):
    # retrieve query string parameters from URL
    ref_id = request.args.get('refereeID', default = None, type = int)
    game_id = request.args.get('gameID', default = None, type = int)

    # error check: ensure that both ref_id and game_id are not null
    if (ref_id is None or game_id is None):
        return jsonify({'message': 'The ref_id and game_id must be provided'}), 400

    # error check: ensure that ref_id is indeed a referee
    if current_user.access is not AccessLevel.referee:
        return jsonify({'message' : 'Invalid access level, needs a referee'}), 401
            
    # connects to the database
    conn = mysql.connect()
    cursor = conn.cursor()

    # calls for the update_ref_schedule procedure
    try: 
        cursor.callproc('post_ref_schedule',[ref_id, game_id])
    except pymysql.MySQLError as err:
        errno = err.args[0]
        print(f'Error number: {errno}')
        if errno == 1452: 
            return  jsonify ({'message': 'gameID or refereeID does not exist'}), 400
        if errno == 1062: 
            return  jsonify ({'message': 'That refereeID is already scheduled to that gameID'}), 400
        
    return jsonify({'message': 'Successfully scheduled a referee to a game'}), 201
