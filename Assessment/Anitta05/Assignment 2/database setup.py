
import sqlite3 as sql

conn = sql.connect('database.db')
cur =conn.cursor()

cur.execute('update student set addr=" NOT NULL" where city=""')
conn.commit()
print("it already exists")