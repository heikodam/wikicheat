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

cursor = get_db()

cursor.execute("SELECT * FROM test")
rows = cursor.fetchall()
print(rows)