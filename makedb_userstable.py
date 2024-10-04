import csv
import sqlite3

conn = sqlite3.connect('userstable.db')
cur = conn.cursor()
cur.execute("""DROP TABLE IF EXISTS userstable""")
cur.execute("""CREATE TABLE userstable (username text, password text, firstname text, lastname text, email text)""")

conn.commit()
conn.close()