import flask

from flaskext.mysql import MySQL

#instaniation
app = flask.Flask(__name__)
app.secret_key= 'secret'

#config
app.config['MYSQL_DATABASE_USER'] = 'b28478beacc7d1'
app.config['MYSQL_DATABASE_PASSWORD'] = 'f364e5eb'
app.config['MYSQL_DATABASE_DB'] = 'heroku_ec53c05b7bfefa2'
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-iron-east-04.cleardb.net'

#init MySQL
mysql = MySQL()
mysql.init_app(app)


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/greg/', methods=['GET'])
def greeg_greg():
    return "<h1>Hello</h1><p>Greg</p>"


app.run()