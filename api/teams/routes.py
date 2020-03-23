from flask import Blueprint

teams = Blueprint('teams', __name__)


@teams.route('/', )
def all_teams():
    return "Teams to be implemented"
