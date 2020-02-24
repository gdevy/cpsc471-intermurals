# app.py
import os
from flask import Flask, request, jsonify
from flaskext.mysql import MySQL
app = Flask(__name__)

app.config['MYSQL_HOST'] = os.environ['MYSQL_HOST']
app.config['MYSQL_USER'] = os.environ['MYSQL_USER']
app.config['MYSQL_PASSWORD'] = os.environ['MYSQL_PASSWORD']
app.config['MYSQL_DB'] = os.environ['MYSQL_DB']

#app.config.from_object(os.environ['APP_SETTINGS'])

mysql = MySQL(app)


# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Hello Kyle Greg Jana</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)