from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3
import os

DATABASE = '/var/www/html/flaskapp/userstable.db'

global_username = ""
global_password = ""

app = Flask(__name__)
app.config.from_object(__name__)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def connect_to_database():
    return sqlite3.connect(app.config['DATABASE'])

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database()
    return db

def execute_query(query, args=()):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows


@app.route('/')
def loginOrRegister():
  return render_template('login.html')


@app.route('/createProfile', methods=['POST'])
def userInfo():
  global global_username
  global global_password
  global_username = request.form['username']
  global_password = request.form['password']

  user = execute_query("""SELECT * FROM userstable WHERE username = ? AND password = ?""",[global_username, global_password])

  if user:
    return redirect(url_for('displayProfile'))
  else:
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""INSERT INTO userstable (username, password) VALUES (?, ?)""",[global_username, global_password])
    conn.commit()
    conn.close()
    return render_template('createProfile.html')


@app.route('/processProfile', methods=['POST'])
def processProfile():
  fname = request.form['firstname']
  lname = request.form['lastname']
  email = request.form['email']
  global global_username
  global global_password
  conn = get_db()
  cur = conn.cursor()
  cur.execute("""UPDATE userstable SET firstname = ?, lastname = ?, email = ? WHERE username = ? AND password = ?""",[fname, lname, email, global_username, global_password])
  conn.commit()
  conn.close()
  return redirect(url_for('displayProfile'))


@app.route('/displayProfile')
def displayProfile():
  global global_username
  global global_password
  if global_username and global_password:
    rows = execute_query("""SELECT * FROM userstable WHERE username = ? AND password = ?""",[global_username, global_password])
    global_username = ""
    global_password = ""
    return render_template('displayProfile.html', username=rows[0][0], password=rows[0][1], firstname=rows[0][2], lastname=rows[0][3], email=rows[0][4])
  else: return render_template('error.html')


@app.route('/viewdb')
def viewdb():
  rows = execute_query("""SELECT * FROM userstable""")
  return '<br>'.join(str(row) for row in rows)


if __name__ == '__main__':
  app.run(debug=True)