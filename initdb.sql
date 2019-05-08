DROP FUNCTION IF EXISTS get_gender_id(text);
DROP FUNCTION IF EXISTS get_user_id(text);
DROP FUNCTION IF EXISTS insert_user(text, text, text, text);

DROP VIEW IF EXISTS mp_start_page;
DROP VIEW IF EXISTS mp_end_page;
DROP VIEW IF EXISTS longest_runtime;
DROP VIEW IF EXISTS most_recent;
DROP VIEW IF EXISTS shortest_runtime;
DROP VIEW IF EXISTS longest_path;

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


-- Function to get the gender id
CREATE OR REPLACE FUNCTION get_gender_id(gender_name TEXT)
RETURNS integer AS $$
BEGIN
RETURN (SELECT gender_id FROM gender WHERE gender = gender_name);
END
$$
LANGUAGE 'plpgsql';

-- Function to get the user id with a email
CREATE OR REPLACE FUNCTION get_user_id(user_email TEXT)
RETURNS integer AS $$
BEGIN
RETURN (SELECT user_id FROM users WHERE email = user_email LIMIT 1);
END 
$$
LANGUAGE 'plpgsql';

-- Function to INSERT a user if he does not yet exits and return his new user_id, otherwise return null
CREATE OR REPLACE FUNCTION insert_user(user_name TEXT, user_email TEXT, user_hash TEXT, gender_name TEXT)
RETURNS integer AS $$
BEGIN
IF get_user_id(user_email) IS NULL THEN
	INSERT INTO users 
	(full_name, email, hash, gender) 
	VALUES (user_name, user_email, user_hash, (get_gender_id(gender_name)));

	RETURN (get_user_id(user_email));
ELSE
	RETURN NULL;
END IF;
							   
END
$$
LANGUAGE 'plpgsql';


-- VIEWS

-- view to get the mp start page
CREATE OR REPLACE VIEW mp_start_page AS
SELECT w.title, COUNT(*) 
        FROM history h
        INNER JOIN wikipages w
        ON start_link = w.wiki_id
        GROUP BY w.title
        ORDER BY COUNT(*) DESC
        LIMIT 1;

-- view get the mp end page
CREATE OR REPLACE VIEW mp_end_page AS 
SELECT w.title, COUNT(*) 
        FROM history h
        INNER JOIN wikipages w
        ON end_link = w.wiki_id
        GROUP BY w.title
        ORDER BY COUNT(*) DESC
        LIMIT 1;

-- view get the longest runtime
CREATE OR REPLACE VIEW longest_runtime AS
SELECT u.full_name AS username, s.title AS Start_Page, e.title AS End_Page, h.degrees_away, h.runtime 
        FROM history h
		INNER JOIN wikipages AS s
		ON h.start_link = s.wiki_id
		INNER JOIN wikipages AS e
		ON h.end_link = e.wiki_id
		INNER JOIN users AS u
		ON h.user_id = u.user_id
        ORDER BY h.runtime DESC
		LIMIT 1;

-- view get the shortest runtime
CREATE OR REPLACE VIEW shortest_runtime AS
SELECT u.full_name AS username, s.title AS Start_Page, e.title AS End_Page, h.degrees_away, h.runtime 
        FROM history h
		INNER JOIN wikipages AS s
		ON h.start_link = s.wiki_id
		INNER JOIN wikipages AS e
		ON h.end_link = e.wiki_id
		INNER JOIN users AS u
		ON h.user_id = u.user_id
        ORDER BY h.runtime ASC
		LIMIT 1;

-- view get the most recent entry in history
CREATE OR REPLACE VIEW most_recent AS
SELECT u.full_name AS username, s.title AS start_page, e.title AS end_page, h.degrees_away, h.runtime 
        FROM history h
		INNER JOIN wikipages AS s
		ON h.start_link = s.wiki_id
		INNER JOIN wikipages AS e
		ON h.end_link = e.wiki_id
		INNER JOIN users AS u
		ON h.user_id = u.user_id
        where h.history_id = (select max(history_id) from history);

-- view get the longest path
CREATE OR REPLACE VIEW longest_path AS
SELECT u.full_name AS username, s.title AS start_page, e.title AS end_age, h.degrees_away, h.runtime 
        FROM history h
		INNER JOIN wikipages AS s
		ON h.start_link = s.wiki_id
		INNER JOIN wikipages AS e
		ON h.end_link = e.wiki_id
		INNER JOIN users AS u
		ON h.user_id = u.user_id
        ORDER BY h.degrees_away DESC, h.runtime ASC
		LIMIT 1;

