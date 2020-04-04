from flask import Blueprint
from api import mysql
import os

main = Blueprint('main', __name__)

#This file can be used for practice if you want. It's not needed


@main.route("/")
@main.route("/home", methods = ['GET'])
def home():
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.callproc('getAllPersons', [])
	data = cursor.fetchall()
	print(data)
	return ' '.join(map(str, [row[0] for row in data]))


@main.route("/about/<name>")
def hello_name(name):
	return "Hello {}!".format(name)

