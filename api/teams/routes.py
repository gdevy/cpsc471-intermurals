from flask import Blueprint, jsonify, request
from api.models import login_required, User, AccessLevel
from api import mysql
import pymysql

teams = Blueprint('teams', __name__)


@teams.route('/', methods = ['POST'])
@login_required
def register_team(current_user: User):
    req = request.json

    team_name = req.get('team_name')
    league_id = req.get('league_id')

    if current_user.access is not AccessLevel.player:
        return jsonify({'message' : 'This end point is for players'}), 400
    
    # connects to the database
    conn = mysql.connect()
    cursor = conn.cursor()

    try: 
        cursor.callproc('register_team', [team_name, current_user.user_id, league_id])
        data = cursor.fetchall()
        print(f'Got: {data}')
    except pymysql.MySQLError as err:
        errno = err.args[0]
        
        if errno == 1452:
            return  jsonify ({'message': 'Provided league_id or player_id does not exist'}), 400
        if errno == 1062: 
            if ("unique_player_per_season" in err.args[1]):
                return  jsonify ({'message': 'The team captain is already registered in this league so they can not register in it again.'}), 400
            
            return  jsonify ({'message': 'That team name is already taken'}), 400
        else: 
            print(f'Error number: {errno}, Error: {err.args[1]}')
            return  jsonify ({'message': 'Something went wrong'}), 500
        
    #call store prod to save team, passing team_name, captain_id, league_id
    return jsonify({'message' : 'Team registered OK'}), 201


@teams.route('/', methods = ['PUT'])
@login_required
def update_team(current_user: User):
    req = request.json
    print(req)

    if current_user.access is not AccessLevel.admin:
        return jsonify({'message' : 'You dont have valid access level, only admin can do this'}), 401
    
    conn = mysql.connect()
    cursor = conn.cursor()

    try: 
        cursor.callproc('update_team', [req.get('team_id'), req.get('captain_id'), req.get('fee_payment', {}).get('league_id'), req.get('fee_payment', {}).get('season_id'), req.get('fee_payment', {}).get('date_paid', None)])
    except pymysql.MySQLError as err:
        errno = err.args[0]
        
        if errno == 1452: 
            return  jsonify ({'message': 'Provided league_id or player_id does not exist'}), 400
        if errno == 1062: 
            return  jsonify ({'message': 'That team name is already taken'}), 400
        else: 
            print(f'Error number: {errno}, Error: {err.args[1]}')
            return  jsonify ({'message': 'Something went wrong'}), 500
    
    new_leagues = req.get('league')
    if new_leagues:
        failed_leagues = []
        for new_league in new_leagues:
            print(f'Adding: {new_league}')
            try:
                cursor.callproc('register_for_league', [new_league.get('league_id'), req.get('team_id'), None])
            except pymysql.MySQLError as err: 
                errno = err.args[0]

                if errno == 1062:
                    failed_leagues.append(new_league.get('league_id'))
                else:
                    print(f'Error number: {errno}, Error: {err.args[1]}')
                    return  jsonify ({'message': 'Something went wrong'}), 500
            
        if failed_leagues:
            return  jsonify ({'message': f'That team is already registered in the following leagues: {failed_leagues}, otherwise OK.'}), 200
    return jsonify({'message' : 'Everything was OK.'}), 201    

@teams.route('/roster/', methods = ['PUT'])
@login_required
def update_team_roster(current_user: User):
    req = request.json
    print(req)
    
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('get_team_captain', [req.get('team_id')])
    data = cursor.fetchall()

    if len(data) != 1:
        return jsonify({'message' : 'Invalid team ID'}), 400

    print(data)
    if data[0][0] != current_user.user_id:   #if current use is not a captain deny access
        return jsonify({'message' : f'Only a captain can do this. Contact {data[0][1]} {data[0][2]} at {data[0][3]}'}), 401
    
    try:
        cursor.callproc('update_team_by_captain', [req.get('team_id'), req.get('captain_id'), req.get('team_name')])
    except pymysql.MySQLError as err: 
        errno = err.args[0]
        print(f'Error number {errno}, Error: {err.args[1]}')


    if req.get('roster'): 
        players_failed = []
        for new_player in req.get('roster'):
            try:
                cursor.callproc('update_team_roster', [req.get('team_id'), new_player.get('player_id')])
            except pymysql.MySQLError as err:
                errno = err.args[0]

                if errno == 1062:
                    players_failed.append(new_player.get('player_id'))
                
                elif errno == 1452:
                    players_failed.append(new_player.get('player_id'))
                else:
                    print(f'Error number {errno}, Error: {err.args[1]}')
                    return jsonify({'message' : 'Something went wrong...'}), 500
        
        if players_failed:
            return  jsonify ({'message': f'Players are already registered in this league, maybe on a different team: {players_failed} (they may not be players), otherwise OK.'}), 200
    
    return jsonify({'message' : 'Updates successful'}), 201  