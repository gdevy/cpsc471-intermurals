from flask import Blueprint

users = Blueprint('users', __name__)


@users.route('/', )
def all_users():
    return "Users to be implemented"