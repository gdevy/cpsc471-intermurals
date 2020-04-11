from flask import Blueprint, jsonify, request
from api.models import login_required, User, AccessLevel
from api import mysql
import pymysql

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
@stats.route('/league/', methods = ['GET'])
def get_standings():
	#get values from the query parameters
	league = request.args.get('league')
	season = request.args.get('season')

	#control to make sure both the season and league are passed as query parameters
	if not season and not league:
		print('error SEASON and LEAGUE parmeters not provided')
		return jsonify({'message' : 'season and league parmaeters not provided'}), 400
	elif not season:
		print('error SEASON parameter not provided')
		return jsonify({'message' : 'season parmeter not provided'}), 400
	elif not league:
		print('error LEAGUE parameter not privided')
		return jsonify({'message' : 'league parmeter not provided'}), 400
	
	#control to make sure the values are integers? Or is this done by the DB?
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.callproc('getStandings2', [league,season])
	data = cursor.fetchall()
	
	#print data to terminal to confirm values
	print(data)
	
	#generate list of results from the database
	standings_list = []
	for i in range(0, len(data)):
		items = {
			'team_name': data[i][0],
			'games_played': data[i][1],
			'wins': data[i][2],
			'losses': data[i][3],
			'win_percentage': data[i][4],
			}
		standings_list.append(items)
	
	#put the list into a dictionary so it can be used by jsonify
	standings_dict = {
		"season": season,
		"league": league,		
		"standings" : standings_list
	}
	return jsonify(standings_dict)
	
	
@stats.route('/player/', methods=['GET'])
def get_player_stat():
	# retrieve query string parameters from URL
	season_id = request.args.get('seasonID', default = None, type = int)
	player_id = request.args.get('playerID', default = None, type = int)
	league_id = request.args.get('leagueID',  default = None, type = int)

	# error check: ensure that player_id is provided
	if not player_id:
		return jsonify({'message': 'The player_id must be provided'}), 400

	# connect to sql database and call get_player_stat stored procedure
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.callproc('get_player_stat', [season_id, player_id, league_id])
	data = cursor.fetchall()

	# map procedure output to a list
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
	
	# store list into a dictionary
	seasons_dict = {
		"seasons" : seasons_list
	}
	return jsonify(seasons_dict)


@stats.route('/team/', methods=['GET'])
def get_team_stat():
	# retrieve query string parameters from URL
	season_id = request.args.get('seasonID', default = None, type = int)
	team_id = request.args.get('teamID', default = None, type = int)
	league_id = request.args.get('leagueID',  default = None, type = int)

	# error check: ensure that player_id is provided
	if team_id is None:
		return jsonify({'message': 'The team_id must be provided'}), 400

	# connect to sql database and call get_player_stat stored procedure
	conn = mysql.connect()
	cursor = conn.cursor()

	cursor.callproc('get_team_stat', [season_id, team_id, league_id])
	data = cursor.fetchall()

	# map procedure output to a list
	seasons_list = []
	for i in range(0, len(data)):
		items = {
			'seasonId': data[i][0],
			'wins': float(data[i][1]),
			'losses': float(data[i][2]),
			'winPercentage': float(data[i][3]),
		}
		seasons_list.append(items)

	seasons_dict = {
		"seasons" : seasons_list
	}
	return jsonify(seasons_dict)

@stats.route('/player/', methods=['PUT'])
@login_required
def update_player_stat(current_user):
    # retrieve query string parameters from URL
	player_id = request.args.get('playerID', default = None, type = int)
	game_id = request.args.get('gameID', default = None, type = int)
	fouls = request.args.get('fouls',  default = None, type = int)
	rebounds = request.args.get('rebounds',  default = None, type = int)
	assists = request.args.get('assists',  default = None, type = int)

	# error check: ensure that both ref_id and game_id are not null
	if (player_id is None or game_id is None):
		return jsonify({'message': 'The playerID and gameID must be provided'}), 400

	# error check: ensure that player_id is indeed a player
	if current_user.access is not AccessLevel.player:
		return jsonify({'message' : 'Invalid access level, needs a player'}), 401
            
	# connects to the database
	conn = mysql.connect()
	cursor = conn.cursor()

    # calls for the update_ref_schedule procedure
	try: 
		cursor.callproc('update_player_stat',[player_id, game_id, fouls, rebounds, assists])
	except pymysql.MySQLError as err:
		errno = err.args[0]
		print(f'Error number: {errno}')
		if errno == 1644: 
			return  jsonify ({'message': 'playerID does not play in a game with gameID'}), 400
		
	return jsonify({'message': 'Successfully updated the game stats'}), 201
