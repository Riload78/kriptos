import sqlite3

connection = sqlite3.connect('cripto.db')
cur = connection.cursor()

f = open('create.sql', 'r')
query = f.read()

try:
    cur.executescript(query)
except sqlite3.Error as e:
    print("Se ha producido un error", e)