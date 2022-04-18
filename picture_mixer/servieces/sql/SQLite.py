import sqlite3

from initSQLite import DATABASE


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def GetData(command):
    conn = get_db_connection()
    posts = conn.execute(command).fetchall()
    conn.close()
    return posts


def addImageToDb(blob):
    return insertData(''' INSERT INTO images(image) VALUES(?) ''', blob)


def getImageFromDb(id):
    return GetData('SELECT * FROM posts WHERE id = ' + id)


def insertData(sql, data):
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute(sql, data)
    connection.commit()
    return cur.lastrowid


