from flask import Blueprint, jsonify, request
from api.models import login_required, User, AccessLevel

teams = Blueprint('teams', __name__)


@teams.route('/', methods = ['POST'])
@login_required
def register_team(current_user):
    req = request.json
    print(req)
    #call store prod to save team, passing team_name, captain_id, league_id
    return jsonify({'message' : 'Needs the Stored Procedure implemented'}), 501


@teams.route('/', methods = ['PUT'])
@login_required
def update_team(current_user: User):
    req = request.json
    print(req)

    if current_user.access is not AccessLevel.admin:
        return jsonify({'message' : 'You dont have valid access level, only admin can do this'}), 401
    
    
    #call store prod to save team, passing team_name, captain_id, league_id
    return jsonify({'message' : 'Needs the Stored Procedure implemented'}), 501    

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