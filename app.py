# app.py
import os
from flask import Flask
from flaskext.mysql import MySQL


app = Flask(__name__)

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = os.environ['MYSQL_USER']
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ['MYSQL_PASSWORD']
app.config['MYSQL_DATABASE_DB'] = os.environ['MYSQL_DB']
app.config['MYSQL_DATABASE_HOST'] = os.environ['MYSQL_HOST']

mysql.init_app(app)

app.config.from_object(os.environ['APP_SETTINGS'])


@app.route('/')
def hello():
	return "Hello World!"


@app.route('/test_db/')
def test_db():
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT version()")
	data = cursor.fetchone()
	return "db connection success"
	
	
@app.route('/<name>')
def hello_name(name):
	return "Hello {}!".format(name)

if __name__ == '__main__':
	app.run()