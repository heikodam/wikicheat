import psycopg2
from db import get_db

cursor = get_db()


fd = open('initdb.sql', 'r')
sqlFile = fd.read()

try:
	cursor.execute(sqlFile)
	print("Database Initilized")
except:
	print("There was an error, Could not initilize")

