from flask import Blueprint, jsonify, request
from api.models import login_required, User, AccessLevel
from api import mysql

stats = Blueprint('stats', __name__)


@stats.route('/game/', methods=['PUT'])
@login_required
def record_game(current_user):
    req = request.json
    print(req)

    if current_user.access is not AccessLevel.referee:
        return jsonify({'message': 'Invalid access level, needs a referee'}), 401

    if False:  # made a db query to see if ref for game_id matches the current ref
        return jsonify({'message': 'The results can only be posted by a game referee'}), 401

    # call stored procedure for storing the game result
    return jsonify({'message': 'Needs the Stored Procedure implemented'}), 501


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
	season_id = request.args.get('seasonID', default = None, type = int)
	player_id = request.args.get('playerID', default = None, type = int)
	league_id = request.args.get('leagueID',  default = None, type = int)

	if not player_id:
		return jsonify({'message': 'The player_id must be provided'}), 400

	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.callproc('get_player_stat', args=(season_id, player_id, league_id))
	data = cursor.fetchall()

	seasons_list = []
	for i in range(0, len(data)):
		items = {
			'seasonId': data[i][6],
			'firstName': data[i][0],
			'lastName': data[i][1],
			'points': float(data[i][2]),
			'fouls': float(data[i][3]),
			'rebounds': float(data[i][4]),
			'assists':  float(data[i][5])
		}
		seasons_list.append(items)
	seasons_dict = {
		"seasons" : seasons_list
	}
	return jsonify(seasons_dict)
