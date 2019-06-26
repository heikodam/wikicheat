import psycopg2
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    connection = psycopg2.connect(
        host = "localhost",
        database = "postgres",
        user = "postgres",
        password = "HDamaske",
        port = 5432
    )
    connection.autocommit=True
 
    cursor = connection.cursor()
    return cursor


def get_record(command):
    cursor = get_db()
    cursor.execute(command)
    rows = cursor.fetchall()
    current_record = {
            "username": rows[0][0],
            "start_page": rows[0][1],
            "end_page": rows[0][2],
            "distance": rows[0][3],
            "runtime": rows[0][4],
        }
    return current_record
