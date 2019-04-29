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
# cursor.execute("SELECT * FROM history")
# row = cursor.fetchall()
# print(row)


cursor.execute("""
DROP TABLE IF EXISTS records;
DROP TABLE IF EXISTS history;
DROP TABLE IF EXISTS wikiPages;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS gender;


CREATE TABLE gender (
	gender_id SERIAL PRIMARY KEY,
	gender varchar(6)
);

INSERT INTO gender (gender) VALUES ('male');
INSERT INTO gender (gender) VALUES ('female');
INSERT INTO gender (gender) VALUES ('other');

CREATE TABLE users (
	user_id SERIAL PRIMARY KEY,
	full_name TEXT,
	email TEXT,
	hash TEXT,
	gender INTEGER REFERENCES gender (gender_id)
);

CREATE TABLE wikiPages (
	wiki_id SERIAL PRIMARY KEY,
	title TEXT UNIQUE
);



CREATE TABLE history (
	history_id SERIAL PRIMARY KEY,
	user_id INTEGER NOT NULL REFERENCES users (user_id),
	start_link INTEGER NOT NULL REFERENCES wikipages (wiki_id),
	end_link INTEGER NOT NULL REFERENCES wikipages (wiki_id),
	degrees_away INTEGER,
	date DATE DEFAULT CURRENT_DATE,
	time TIME DEFAULT CURRENT_TIME,
	runtime NUMERIC
);



CREATE TABLE records (
	record_id SERIAL PRIMARY KEY,
	type_of_record TEXT NOT NULL,
	history_id INTEGER REFERENCES history(history_id)
);

INSERT INTO users (full_name, email, hash, gender) VALUES ('Jack', 'jack@gmail.com', '1234', (SELECT gender_id FROM gender WHERE gender = 'male'));

INSERT INTO wikipages (title) VALUES ('Switzerland');
INSERT INTO wikipages (title) VALUES ('Bern');
INSERT INTO history (user_id, start_link, end_link, degrees_away, runtime) VALUES (1, 1, 1, 1, 0.9);

INSERT INTO records (type_of_record, history_id) VALUES ('longest_runtime', 1);
INSERT INTO records (type_of_record, history_id) VALUES ('shortest_runtime', 1);
INSERT INTO records (type_of_record, history_id) VALUES ('longest_path', 1);
INSERT INTO records (type_of_record, history_id) VALUES ('most_recent', 1);


""")
