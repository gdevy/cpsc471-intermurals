from flask import Blueprint, jsonify, request
from api.models import login_required, User, AccessLevel
from api import mysql
import pymysql

schedule = Blueprint('schedule', __name__)


@schedule.route('/game/', methods = ['POST','PUT'])
@login_required
def record_game(current_user):
	req = request.json
	
	#check to see if it is a PUT method
	if request.method == 'PUT':
		if current_user.access is not AccessLevel.referee:
			return jsonify({'message' : 'Invalid access level, needs a referee'}), 401
		if False: #made a db query to see if ref for game_id matches the current ref
				return jsonify({'message' : 'The results can only be posted by a game referee'}), 401
			
		#call stored procedure for storing the game result
		return jsonify({'message' : 'Needs the Stored Procedure implemented'}), 501
	
	#check to see if it is a POST method
	elif request.method == 'POST':
		
		#check access level
		if current_user.access is not AccessLevel.admin:
			return jsonify({'message' : 'Invlaid access level, requires admin token'}), 401
		conn = mysql.connect()
		cursor = conn.cursor()


		#validate body
		for i in range(0,len(req['games'])):
			if not req['games'][i]['home']:
				return jsonify({'message' : 'The home team Id must be provided for game at index: ' + str(i)}), 400
			if not req['games'][i]['away']:
				return jsonify({'message' : 'The away team Id must be provided at index: ' + str(i)}), 400
			if not req['games'][i]['date']:
				return jsonify({'message' : 'The date of the game must be provided at index: ' + str(i)}), 400
			if not req['games'][i]['location']:
				return jsonify({'message' : 'The location Id of the game must be provided at index: ' + str(i)}), 400
			if not req['games'][i]['season']:
				return jsonify({'message' : 'The season Id for the teams must be provided at index: ' + str(i)}), 400
		
		#iterate through the games list
		for i in range(0,len(req['games'])):

			#call stored procedure for each game
			try:
				cursor.callproc('post_game_schedule',[req['games'][i]['home'], req['games'][i]['away'], req['games'][i]['date'], req['games'][i]['location'], req['games'][i]['season']])
			except pymysql.MySQLError as err:
				errno = err.args[0]
				print(f'Error number: {errno}')
				#get errors for if the body is invalid
				return jsonify({'message' : 'Threw an error need error code'}), 501
			print('Updated Games\n')
		
		return jsonify({'message' : 'Updated the game schedule in the Data Base'}), 501


@schedule.route('/referee/', methods = ['POST'])
@login_required
def post_ref_schedule(current_user):
    # retrieve query string parameters from URL
    ref_id = request.args.get('refereeID', default = None, type = int)

    # retrieve query string parameters from URL and user_id from current_user
    ref_id = current_user.user_id
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