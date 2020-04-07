from flask import Blueprint, jsonify, request
from api.models import login_required, User, AccessLevel

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
    #write control to make sure we have a league and a season passed into the query parameters.
     
    # print(league)
    # print(season)
    return jsonify({'message' : 'Not a valid league OR season'}), 400
    conn = mysql.connect()
    cursor = conn.cursor()
    #try
    #args = (league_id,season_id)
    #cursor.callproc('getStandings2, args)
    
    cursor.callproc('getStandings2', [league_id,season_id])
    data = cursor.fetchall()
    print(data)
  
    #return ' '.join(map(str, [row[0] for row in data]))
	
	