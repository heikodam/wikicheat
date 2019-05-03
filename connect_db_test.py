import psycopg2


def get_db():
    connection = psycopg2.connect(
        host = "35.242.229.99",
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

# cursor = get_db()

# cursor.execute("SELECT get_gender_id('male');")
# id = cursor.fetchall()[0][0]
# print(id)

# def close_db(e=None):
#     db = g.pop('db', None)

#     if db is not None:
#         db.close()

# connection.close()