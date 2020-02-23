# app.py
from flask import Flask, request, jsonify
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'MyDB'

mysql = MySQL(app)

@app.route('/getmsg/', methods=['GET'])
def check_db_connection():
    
    return "<h1>" + 


# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Hello Kyle Greg Jana</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)