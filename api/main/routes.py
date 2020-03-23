from flask import Blueprint
from api import mysql
import os

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home", method = ['GET'])
def home():
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute("SELECT member_name FROM " + os.environ['MYSQL_DB'] + ".test_table;")
	data = cursor.fetchall()
	return ' '.join(map(str, [name[0] for name in data]))


@main.route("/about/<name>")
def hello_name(name):
	return "Hello {}!".format(name)