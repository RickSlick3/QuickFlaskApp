from collections import Counter
import csv
import sqlite3
from flask import Flask, request, g, redirect, url_for

DATABASE = '/var/www/html/flaskapp/userstable.db'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_to_database():
  return sqlite3.connect(app.config['DATABASE'])

def get_db():
  db = getattr(g, 'db', None)
  if db is None:
    db = g.db = connect_to_database()
  return db

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, 'db', None)
  if db is not None:
    db.close()

def execute_query(query, args=()):
  cur = get_db().execute(query, args)
  rows = cur.fetchall()
  cur.close()
  return rows

@app.route("/log-in-or-register")
def logInOrRegister():
  uname = request.form.get('username')
  pword = request.form.get('password')
  
  userRow = execute_query("""SELECT * FROM userstable WHERE username = ? AND password = ?""",[uname, pword])
  
  if userRow:
    return redirect(url_for('displayProfile'))
  else:
    return redirect(url_for('createProfile'))

@app.route("/create-profile")
def createProfile(uname, pword):
  return

@app.route("/display-profile")
def displayProfile(uname, pword):
  userRow = execute_query("""SELECT * FROM userstable WHERE username = ? AND password = ?""",[uname, pword])
  return '<br>'.join(str(row) for row in userRow)

@app.route("/viewdb")
def viewdb():
  rows = execute_query("""SELECT * FROM natlpark""")
  return '<br>'.join(str(row) for row in rows)

@app.route("/state/<state>")
def state_query(state):
  rows = execute_query("""SELECT * FROM natlpark WHERE state = ?""",[state.title()])
  return '<br>'.join(str(row) for row in rows)


if __name__ == '__main__':
    app.run()