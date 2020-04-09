from flask import Blueprint, jsonify, request
from api.models import login_required, User, AccessLevel

schedule = Blueprint('schedule', __name__)


@schedule.route('/game/', methods = ['PUT'])
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


    @schedule.route('/referee/', methods = ['PUT'])
    @login_required
    def update_ref_schedule(current_user):
        ref_id = request.args.get('refereeID', default = None, type = int)
        game_id = request.args.get('gameID', default = None, type = int)

        if (not ref_id or not game_id):
            return jsonify({'message': 'The ref_id and game_id must be provided'}), 400

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('update_ref_schedule', args=(ref_id, game_id))
        if (not cursor.fetchall):
            return jsonify({'message': 'The provided ref_id and game_id does not exist'}), 400

        return "hi"
