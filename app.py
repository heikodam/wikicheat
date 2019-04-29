#external imports
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify, url_for
from werkzeug.security import generate_password_hash, check_password_hash
#from flask_sqlalchemy import SQLAlchemy
import os
import psycopg2
import time
#import json

#my imports
from connect_db_test import get_db
# from live_finder import *
from web_scraper import checkIfExsits
from fast import degree_distance


app = Flask(__name__)
app.secret_key = "mysupersecretkey"
# app.config[os.urandom(12)]
#db = SQLAlchemy(app)


@app.route("/")
def home():
    if "user_id" in session:
        return redirect("/wikicheat")
    else:
        return redirect("/login")
    

@app.route("/register",  methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        entered_name = request.form['full_name']
        entered_email = request.form['email']
        entered_password = request.form['password']
        entered_confirm_password = request.form['confirm_password']
        entered_gender = request.form.get('gender', None)


        if not entered_name or not entered_email or not entered_password or not entered_confirm_password or not entered_gender:
            return render_template("registration.html", errormessage = "You did not enter fill out all the fields")
        if entered_password != entered_confirm_password:
            return render_template("registration.html", errormessage = "The Passwords you entered did not match")
        
        #get data from db
        cursor = get_db()
        
        #check if email already exists
        cursor.execute("SELECT email FROM users WHERE email = '{}' ".format(entered_email))

        user = cursor.fetchall()
        if len(user) > 0:
            return render_template("registration.html", errormessage = "There is already an email assigned to this account")

        hash = generate_password_hash(entered_password)
        cursor.execute("SELECT gender_id FROM gender WHERE gender='{}'".format(entered_gender))
        gender_id = cursor.fetchall()[0][0]
        cursor.execute("INSERT INTO users (full_name, email, hash, gender) VALUES ('{}', '{}', '{}', '{}');".format(entered_name, entered_email, hash, gender_id))

        cursor.execute("SELECT user_id FROM users WHERE email ='{}' ".format(entered_email))
        user_id = cursor.fetchall()[0][0]

        session['user_id'] = user_id
        session['user_engagement'] = { "event": "engagement", "user_id": user_id, "games_played": 0}
        dataLayer = {"event": "newUser", "user_id": user_id, "newUser": "New User"}
        session['dataLayer'] = dataLayer

        return redirect("/wikicheat")


        
    else:
        if "user_id" in session:
            return redirect("/wikicheat")
        return render_template("registration.html")

 
@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        #get data from form
        entered_email = request.form['email']
        entered_password = request.form['password']

        #check if data exsists
        if not entered_email or not entered_password:
            return render_template("login.html", errormessage = "You did not enter the write Data")

        #get data from db
        cursor = get_db()

        cursor.execute("SELECT user_id, email, hash, full_name FROM users WHERE email = '{}' ".format(entered_email))
        user = cursor.fetchall()
        
        if len(user) == 1:
            user_id = user[0][0]
            db_email = user[0][1]
            db_hash = user[0][2]
            db_name = user[0][3]
            if db_email == entered_email and check_password_hash(db_hash, entered_password):
                session['user_id'] = user_id
                session['user_engagement'] = {"event": "engagement", "user_id": user_id, "games_played": 0}
                session['dataLayer'] = {"event": "newUser", "user_id": user_id, "newUser": "Returning User", }
                return redirect("/wikicheat")
            else:
                return render_template("login.html", errormessage = "You entered the wrong login information")
        else:
            return render_template("login.html", errormessage = "Sorry, You entered the wrong email address")

    else:
        if "user_id" in session:
            return redirect("/wikicheat")

        return render_template("login.html")


@app.route("/logout")
def logout():
    if 'user_id' in session:
        session.pop('user_id', None)
    return redirect("/")
 

@app.route('/wikicheat', methods=('GET', 'POST'))
def wikiCheat():
    if request.method == 'POST':
        start_link = request.form['start_link'].replace(" ", "_")
        end_link = request.form['end_link'].replace(" ", "_")

        if not start_link or not end_link:
            return render_template("wikicheat.html", errormessage = "Please enter 2 Valid Values")
        elif not checkIfExsits(start_link):
            return render_template("wikicheat.html", errormessage = "The first link you enterd does not exsits")
        elif not checkIfExsits(end_link):
            return render_template("wikicheat.html", errormessage = "The second link you enterd does not exsits")
        elif start_link == end_link:
            return render_template("wikicheat.html", errormessage = "Please enter two different links")


        start_time = time.time()
        path_length = degree_distance(start_link, end_link)
        runtime = round(time.time() - start_time, 3)

        user_id = session['user_id']
        cursor = get_db()
        cursor.execute("INSERT INTO wikipages (title) VALUES ('{0}') ON CONFLICT DO NOTHING;".format(start_link))
        cursor.execute("INSERT INTO wikipages (title) VALUES ('{0}') ON CONFLICT DO NOTHING;".format(end_link))
        cursor.execute("""INSERT INTO history (user_id, start_link, end_link, degrees_away, runtime) 
                        VALUES (
                            {user_id},
                            (SELECT wiki_id FROM wikiPages WHERE title='{start_link}'),
                            (SELECT wiki_id FROM wikiPages WHERE title='{end_link}'),
                            {degrees_away},
                            {runtime}
                        );""".format(user_id=user_id, start_link=start_link, end_link=end_link, degrees_away=path_length, runtime=runtime))

        cursor.execute("SELECT MAX(history_id) FROM history;")        
        history_id = cursor.fetchall()[0][0]

        #check all records
        cursor.execute("SELECT r.type_of_record, h.degrees_away ,h.runtime FROM records r LEFT JOIN history h ON r.history_id = h.history_id;")
        records = cursor.fetchall()
        for record in records:
            if record[0] == 'longest_runtime' and runtime > record[2]:
                cursor.execute("UPDATE records SET history_id={} WHERE type_of_record = '{}';".format(history_id, "longest_runtime"))
            if record[0] == 'shortest_runtime' and runtime < record[2]:
                cursor.execute("UPDATE records SET history_id={} WHERE type_of_record = '{}';".format(history_id, "shortest_runtime"))
            if record[0] == 'longest_path' and path_length > record[1]:
                cursor.execute("UPDATE records SET history_id={} WHERE type_of_record = '{}';".format(history_id, "longest_path"))
            #Update most recent history
            cursor.execute("UPDATE records SET history_id={} WHERE type_of_record = '{}';".format(history_id, "most_recent"))

        cursor.close()

        dataLayer = {"event": "wikicheat", "user_id": user_id}
        session['user_engagement']['games_played'] += 1
        session.modified = True
        result = {"start_link": start_link, "end_link": end_link, "path_length": path_length, "runtime": runtime}
        return render_template("wikicheat.html", result = result, dataLayer=dataLayer)

    else: 
        if 'user_id' in session:
            dataLayer = None
            if 'dataLayer' in session:
                dataLayer = session.pop('dataLayer')
            return render_template("wikicheat.html", dataLayer=dataLayer)
        else:
            return redirect("/")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/settings', methods=('GET', 'POST'))
def settings():
    if request.method == 'POST':
        entered_data = {}
        entered_data['full_name'] = request.form['full_name']
        entered_data['email'] = request.form['email']
        entered_data['old_password'] = request.form['old_password']
        entered_data['new_password'] = request.form['password']
        entered_data['confirm_password'] = request.form['confirm_password']
        entered_data['gender'] = request.form.get('gender', None)
        
        cursor = get_db()
        user_id = session['user_id']
        cursor.execute("""SELECT u.full_name, u.email, u.hash, d.gender FROM users u 
                                JOIN gender d 
                                ON u.gender = d.gender_id
                                WHERE user_id = {};  
                                """.format(user_id))
        user = cursor.fetchall()
        personal_data = {}
        personal_data["full_name"] = user[0][0]
        personal_data["email"] = user[0][1]
        personal_data["old_hash"] = user[0][2]
        personal_data["gender"] = user[0][3]


        if personal_data['full_name'] != entered_data['full_name']:
            cursor.execute("UPDATE users SET full_name = '{}' WHERE user_id = {};".format(entered_data['full_name'], user_id))
        if personal_data['email'] != entered_data['email']:
            cursor.execute("UPDATE users SET email = '{}' WHERE user_id = {};".format(entered_data['email'], user_id))
        if personal_data['gender'] != entered_data['gender']:
            cursor.execute("UPDATE users SET gender = (SELECT gender_id FROM gender WHERE gender = '{}') WHERE user_id = {};".format(entered_data['gender'], user_id))

        

        if check_password_hash(personal_data['old_hash'], entered_data['old_password']):
            if not entered_data['new_password'] or not entered_data['confirm_password'] or entered_data['new_password'] != entered_data['confirm_password']:
                return render_template("settings.html", errormessage = 'There was a error with the Passwords you entered')
            else:
                new_hash = generate_password_hash(entered_data['new_password'])
                cursor.execute("UPDATE users SET hash = '{}' WHERE user_id = {};".format(new_hash, user_id))

        return redirect("/")

    
    else:
        if 'user_id' in session:

            #get data from db
            cursor = get_db()
            user_id = session['user_id']
            cursor.execute("""SELECT u.full_name, u.email, d.gender FROM users u 
                                JOIN gender d 
                                ON u.gender = d.gender_id
                                WHERE user_id = {};  
                                """.format(user_id))
            user = cursor.fetchall()
            personal_data = {}
            personal_data["full_name"] = user[0][0]
            personal_data["email"] = user[0][1]
            personal_data[user[0][2]] = "checked"

            return render_template("settings.html", personal_data = personal_data)
        else:
            return redirect("/")

@app.route('/statistics', methods=('GET', 'POST'))
def statistics():
    if "user_id" in session:

        cursor = get_db()
        user_id = session['user_id']
        records = []

        cursor.execute("""SELECT r.type_of_record, u.full_name, h.runtime, s.title AS start_link, e.title AS end_link,  h.degrees_away
                            FROM records r 
                            LEFT JOIN history h 
                            ON r.history_id = h.history_id 
                            INNER JOIN users u
                            ON h.user_id = u.user_id
                            INNER JOIN wikiPages s
                            ON h.start_link = s.wiki_id
							INNER JOIN wikiPages e
                            ON h.end_link = e.wiki_id;""")
        db_records = cursor.fetchall()
        users_records = {}
        for record in db_records:
            print(record)
            users_records[record[0]] = {
                        "username": record[1],
                        "runtime": record[2],
                        "start_page": record[3],
                        "end_page": record[4],
                        "distance": record[5]
                    } 
            


        cursor.execute("""
        SELECT w.title, COUNT(*) 
        FROM history h
        INNER JOIN wikipages w
        ON start_link = w.wiki_id
        GROUP BY w.title
        ORDER BY COUNT(*) DESC
        LIMIT 1;
        """)
        db_start_page = cursor.fetchall()

        cursor.execute("""
        SELECT w.title, COUNT(*) 
        FROM history h
        INNER JOIN wikipages w
        ON end_link = w.wiki_id
        GROUP BY w.title
        ORDER BY COUNT(*) DESC
        LIMIT 1;
        """)
        db_end_page =cursor.fetchall()

        page_records = {
            "start_link_record": {"title": db_start_page[0][0], "amount": db_start_page[0][1]},
            "end_link_record": {"title": db_end_page[0][0], "amount": db_end_page[0][1]}
        }


        print(users_records)
        return render_template("statistics.html", users_records = users_records, page_records = page_records)
    else:
        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=80)