from flask import Blueprint, jsonify, request
from api.models import login_required, User, AccessLevel
from api import mysql
import json
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