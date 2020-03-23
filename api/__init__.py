from flask import Flask
from flask_bcrypt import Bcrypt
from flaskext.mysql import MySQL
from config import Config

bcrypt = Bcrypt()
mysql = MySQL()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    mysql.init_app(app)
    bcrypt.init_app(app)

    # from api.teams.routes import teams
    # from api.users.routes import users
    # from api.players.routes import players
    from api.main.routes import main

    # app.register_blueprint(users)
    # app.register_blueprint(posts)
    app.register_blueprint(main)

    return app