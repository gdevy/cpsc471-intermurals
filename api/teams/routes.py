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
                cursor.callproc('register_for_league', [new_league.get('league_id'), req.get('team_id')])
            except pymysql.MySQLError as err: 
                errno = err.args[0]

                if errno == 1062:
                    failed_leagues.append(new_league.get('league_id'))
                else:
                    print(f'Error number: {errno}, Error: {err.args[1]}')
                    return  jsonify ({'message': 'Something went wrong'}), 500
            
        if failed_leagues:
            return  jsonify ({'message': f'That team is already registered in the following leagues: {failed_leagues}, otherwise OK.'}), 500
    return jsonify({'message' : 'Everything was OK.'}), 201    

@teams.route('/roster/', methods = ['PUT'])
@login_required
def update_team_roster(current_user: User):
    req = request.json
    print(req)
    
    #make db query to get team_id based on team captain_id
    if False:   #if current use is not a captain deny access
        return jsonify({'message' : 'You dont have valid access level, only team captains can do this'}), 401
    
    if req.get('team_name'):    #if team name was specified
        print(f'Updating team name to {req["team_name"]}')    #call team name stored proc using captains team_id

    if req.get('captain_id'): #if captain_id was specified
        print(f'Updating captain_id to name to {req["captain_id"]}')    #update the captain of team associated with current_user

    if req.get('roster'): #if a roster was provided
        print(f'Putting following players into team: {req["roster"]}')  #call roster stored proc
    

    return jsonify({'message' : 'Needs the Stored Procedures implemented'}), 501  