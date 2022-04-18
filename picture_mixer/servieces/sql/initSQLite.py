import sqlite3

DATABASE = 'AbstractVisioner.db'

connection = sqlite3.connect(DATABASE)

with open('init.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()