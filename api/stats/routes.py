from flask import Blueprint, jsonify, request
from api.models import login_required, User, AccessLevel
from api import mysql

stats = Blueprint('stats', __name__)


@stats.route('/game/', methods = ['PUT'])
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


#public route
@stats.route('/league/?league&season', methods = ['GET'])
def get_standings(league_id,season_id):

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('getStandings2', [league_id,season_id])
    data = cursor.fetchall()
    print(data)
    return jsonify({'message' : 'Not a valid league OR season'}), 400
    #return ' '.join(map(str, [row[0] for row in data]))
	
	
@stats.route('/player/', methods=['GET'])
def get_player_stat():
	season_id  = request.args.get('seasonID')
	player_id = request.args.get('playerID')
	league_id = request.args.get('leagueID')


	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.callproc('get_player_stat1', args=(season_id, player_id, league_id))
	data = cursor.fetchone()
	return jsonify(
        {
        'firstName' : data[0],
        'lastName' : data[1],
        'points' : float(data[2]),
        'rebounds' : float(data[3]),
        'assists' :  float(data[4])
        }
    )

