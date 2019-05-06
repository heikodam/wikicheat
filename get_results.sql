-- Get the most recent entry in history
SELECT u.full_name AS username, s.title AS start_page, e.title AS end_page, h.degrees_away, h.runtime 
        FROM history h
		JOIN wikipages AS s
		ON h.start_link = s.wiki_id
		JOIN wikipages AS e
		ON h.end_link = e.wiki_id
		JOIN users AS u
		ON h.user_id = u.user_id
        where h.history_id = (select max(history_id) from history);


-- Get the longest Runtime
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


-- Get the shortest Runtime
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


-- Get the longest path
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


-- Get the most popular start pages
SELECT w.title, COUNT(*) 
        FROM history h
        INNER JOIN wikipages w
        ON start_link = w.wiki_id
        GROUP BY w.title
        ORDER BY COUNT(*) DESC
        LIMIT 1;


-- Get the most popular end page
SELECT w.title, COUNT(*) 
        FROM history h
        INNER JOIN wikipages w
        ON end_link = w.wiki_id
        GROUP BY w.title
        ORDER BY COUNT(*) DESC
        LIMIT 1;



-- FUNCTIONS


-- Function to get the gender id
DROP FUNCTION IF EXISTS get_gender_id(text);
CREATE OR REPLACE FUNCTION get_gender_id(gender_name TEXT)
RETURNS integer AS $$
BEGIN
RETURN (SELECT gender_id FROM gender WHERE gender = gender_name);
END
$$
LANGUAGE 'plpgsql';

-- Function get the mp start page
DROP FUNCTION IF EXISTS get_mp_start_page();
CREATE OR REPLACE FUNCTION get_mp_start_page()
RETURNS Table(
	title TEXT,
	amount BIGINT
)
AS $$
BEGIN
RETURN QUERY
SELECT w.title, COUNT(*) 
        FROM history h
        INNER JOIN wikipages w
        ON start_link = w.wiki_id
        GROUP BY w.title
        ORDER BY COUNT(*) DESC
        LIMIT 1;
END
$$
LANGUAGE 'plpgsql';

-- SELECT * FROM get_mp_start_page();

-- function get the mp end page
DROP FUNCTION IF EXISTS get_mp_start_page();
CREATE OR REPLACE FUNCTION get_mp_start_page()
RETURNS Table(
	title TEXT,
	amount BIGINT
)
AS $$
BEGIN
RETURN QUERY
SELECT w.title, COUNT(*) 
        FROM history h
        INNER JOIN wikipages w
        ON end_link = w.wiki_id
        GROUP BY w.title
        ORDER BY COUNT(*) DESC
        LIMIT 1;
END
$$
LANGUAGE 'plpgsql';
-- SELECT * FROM get_mp_end_page();


-- function get the most_recent entry
DROP FUNCTION IF EXISTS get_most_recent();
CREATE OR REPLACE FUNCTION get_most_recent()
RETURNS Table(
	username TEXT,
	start_page TEXT,
	end_page TEXT,
	degrees_away INT,
	runtime NUMERIC
)
AS $$
BEGIN
RETURN QUERY
SELECT u.full_name AS username, s.title AS start_page, e.title AS end_page, h.degrees_away, h.runtime 
        FROM history h
		JOIN wikipages AS s
		ON h.start_link = s.wiki_id
		JOIN wikipages AS e
		ON h.end_link = e.wiki_id
		JOIN users AS u
		ON h.user_id = u.user_id
        where h.history_id = (select max(history_id) from history);
END
$$
LANGUAGE 'plpgsql';

-- function get the longest_path
CREATE OR REPLACE FUNCTION get_longest_path()
RETURNS Table(
	username TEXT,
	start_page TEXT,
	end_page TEXT,
	degrees_away INT,
	runtime NUMERIC
)
AS $$
BEGIN
RETURN QUERY
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
END
$$
LANGUAGE 'plpgsql';

-- function get the longest runtime
CREATE OR REPLACE FUNCTION get_longest_runtime()
RETURNS Table(
	username TEXT,
	start_page TEXT,
	end_page TEXT,
	degrees_away INT,
	runtime NUMERIC
)
AS $$
BEGIN
RETURN QUERY
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
END
$$
LANGUAGE 'plpgsql';

-- function get the shortest runtime
CREATE OR REPLACE FUNCTION get_shortest_runtime()
RETURNS Table(
	username TEXT,
	start_page TEXT,
	end_page TEXT,
	degrees_away INT,
	runtime NUMERIC
)
AS $$
BEGIN
RETURN QUERY	
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
END
$$
LANGUAGE 'plpgsql';



-- VIEWS

-- view to get the mp start page
DROP VIEW IF EXISTS mp_start_page;
CREATE OR REPLACE VIEW mp_start_page AS
SELECT w.title, COUNT(*) 
        FROM history h
        INNER JOIN wikipages w
        ON start_link = w.wiki_id
        GROUP BY w.title
        ORDER BY COUNT(*) DESC
        LIMIT 1;

-- view get the mp end page
DROP VIEW IF EXISTS mp_end_page;
CREATE OR REPLACE VIEW mp_end_page AS 
SELECT w.title, COUNT(*) 
        FROM history h
        INNER JOIN wikipages w
        ON end_link = w.wiki_id
        GROUP BY w.title
        ORDER BY COUNT(*) DESC
        LIMIT 1;

-- view get the longest runtime
DROP VIEW IF EXISTS longest_runtime;
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
DROP VIEW IF EXISTS shortest_runtime;
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
DROP VIEW IF EXISTS most_recent;
CREATE OR REPLACE VIEW most_recent AS
SELECT u.full_name AS username, s.title AS start_page, e.title AS end_page, h.degrees_away, h.runtime 
        FROM history h
		JOIN wikipages AS s
		ON h.start_link = s.wiki_id
		JOIN wikipages AS e
		ON h.end_link = e.wiki_id
		JOIN users AS u
		ON h.user_id = u.user_id
        where h.history_id = (select max(history_id) from history);

-- view get the longest path
DROP VIEW IF EXISTS longest_path;
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