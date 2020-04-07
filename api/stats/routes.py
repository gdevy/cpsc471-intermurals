from flask import Blueprint, jsonify, request
from api.models import login_required, User, AccessLevel, Standing
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
    league = request.args.get('league')
    season = request.args.get('season')
    
    #control to make sure we have a league and a season as query parameters.
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
    #try
    #args = (league_id,season_id)
    #cursor.callproc('getStandings2, args)
    
    cursor.callproc('getStandings2', [league,season])
    data = cursor.fetchall()
    print(data)

    #These and variations did not work
        # return jsonify(data)
        # return ' '.join(map(str, [ row[0] for row in data]))
        # return jsonify(parse_standings(data))
        # return json.dumps(parse_standings(data).__dict__)
    
    displayData = parse_standings(data)
    return json.dumps(displayData, default=lambda o: o.__dict__, indent=4)
    
    #this one printed them all in line
        # return '\n'.join(map(str, [json.dumps(row.__dict__) for row in displayData]))
	
def parse_standings(data):
    result = []
    for row in data:
        print(row)
        print(row[0])
        result.append(Standing(row[0],row[1],row[2],row[3],row[4]))
    return result 