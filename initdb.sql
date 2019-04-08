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
	runtime TIME
);

CREATE TABLE records (
	record_id SERIAL PRIMARY KEY,
	type_of_record TEXT NOT NULL,
	history_id INTEGER REFERENCES history(history_id)
);



-- Insert some test data
-- INSERT INTO wikipages (title) VALUES ('Test');
-- INSERT INTO wikipages (title) VALUES ('Second_Test');
-- INSERT INTO history (user_id, start_link, end_link, degrees_away, runtime) VALUES (11, 1, 1, 2, '00:02:21');
-- SELECT * FROM history;



-- INSERT INTO history (user_id, start_link, end_link, degrees_away, runtime) VALUES (11, 1, 1, 2, '00:02:21');


--INSERT INTO users (full_name, email, hash, gender) VALUES ('Heiko Damaske', 'heiko.damaske@gmail.com', '1234', (SELECT gender_id FROM gender WHERE gender = 'male'))