import csv
import sqlite3

conn = sqlite3.connect('userstable.db')
cur = conn.cursor()
cur.execute("""DROP TABLE IF EXISTS userstable""")
cur.execute("""CREATE TABLE userstable (username text, password text, firstname text, lastname text, email text)""")

with open('userstable.csv', 'r') as f:
  reader = csv.reader(f.readlines()[1:])  # exclude header line
  cur.executemany("""INSERT INTO userstable VALUES (?,?,?,?,?)""",(row for row in reader))

conn.commit()
conn.close()