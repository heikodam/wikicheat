#external imports
from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify, url_for
from werkzeug.security import generate_password_hash, check_password_hash
#from flask_sqlalchemy import SQLAlchemy
import os
import psycopg2
import time

#my imports
from connect_db_test import *
from web_scraper import checkIfExsits
from fast import degree_distance
from wikicheat import *


app = Flask(__name__)
app.secret_key = "mysupersecretkey"


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
        cursor.execute("SELECT email FROM users WHERE email = %s ", (entered_email, ))

        user = cursor.fetchall()
        if len(user) > 0:
            return render_template("registration.html", errormessage = "There is already an email assigned to this account")

        hash = generate_password_hash(entered_password)
        cursor.execute("SELECT get_gender_id(%s);", (entered_gender,))
        gender_id = cursor.fetchall()[0][0]
        cursor.execute("INSERT INTO users (full_name, email, hash, gender) VALUES (%s, %s, %s, %s);", (entered_name, entered_email, hash, gender_id, ))

        cursor.execute("SELECT user_id FROM users WHERE email = %s ", (entered_email, ))
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

        cursor.execute("SELECT user_id, email, hash, full_name FROM users WHERE email = %s ", (entered_email, ))
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
                                WHERE user_id = %s;  
                                """, (user_id,))
        user = cursor.fetchall()
        personal_data = {}
        personal_data["full_name"] = user[0][0]
        personal_data["email"] = user[0][1]
        personal_data["old_hash"] = user[0][2]
        personal_data["gender"] = user[0][3]


        if personal_data['full_name'] != entered_data['full_name']:
            cursor.execute("UPDATE users SET full_name = %s WHERE user_id = %s;", (entered_data['full_name'], user_id, ))
        if personal_data['email'] != entered_data['email']:
            cursor.execute("UPDATE users SET email = %s WHERE user_id = %s",(entered_data['email'], user_id,))
        if personal_data['gender'] != entered_data['gender']:
            cursor.execute("UPDATE users SET gender = (SELECT get_gender_id(%s)) WHERE user_id = %s;",(entered_data['gender'], user_id, ))

        

        if check_password_hash(personal_data['old_hash'], entered_data['old_password']):
            if not entered_data['new_password'] or not entered_data['confirm_password'] or entered_data['new_password'] != entered_data['confirm_password']:
                return render_template("settings.html", errormessage = 'There was a error with the Passwords you entered')
            else:
                new_hash = generate_password_hash(entered_data['new_password'])
                cursor.execute("UPDATE users SET hash = %s WHERE user_id = %s;",(new_hash, user_id,))

        return redirect("/")

    
    else:
        if 'user_id' in session:

            #get data from db
            cursor = get_db()
            user_id = session['user_id']
            cursor.execute("""SELECT u.full_name, u.email, d.gender FROM users u 
                                JOIN gender d 
                                ON u.gender = d.gender_id
                                WHERE user_id = %s;  
                                """, (user_id, ))
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

        users_records = {}

        users_records['most_recent'] = get_record("SELECT * FROM get_most_recent();")
        users_records['longest_path'] = get_record("SELECT * FROM get_longest_path();")
        users_records['longest_runtime'] = get_record("SELECT * FROM get_longest_runtime();")
        users_records['shortest_runtime'] = get_record("SELECT * FROM get_shortest_runtime();")

        cursor.execute("SELECT * FROM get_mp_start_page();")
        db_start_page = cursor.fetchall()

        cursor.execute("SELECT * FROM get_mp_end_page();")
        db_end_page =cursor.fetchall()

        page_records = {
            "start_link_record": {"title": db_start_page[0][0], "amount": db_start_page[0][1]},
            "end_link_record": {"title": db_end_page[0][0], "amount": db_end_page[0][1]}
        }


        print(users_records)
        return render_template("statistics.html", users_records = users_records, page_records = page_records)
    else:
        return redirect("/")


#finds the shortest path and sends json object with the results
@app.route('/find_path')
def get_post_javascript_data():
    # start_link = request.form['start_link']
    start_link = request.args.get('start_link', '', type=str)
    end_link = request.args.get('end_link', '', type=str)

    if not start_link or not end_link:
        return jsonify({"error": "Please enter 2 Valid Values"})
    elif not checkIfExsits(start_link):
        print("retunring now")
        return jsonify({"error": "The first link you enterd does not exsits"})
    elif not checkIfExsits(end_link):
        return jsonify({"error": "The second link you enterd does not exsits"})
    elif start_link == end_link:
        return jsonify({"error": "Please enter two different links"})

    distance, time = wikicheat(start_link, end_link)

    
    return jsonify({'start_link': start_link, 'end_link': end_link, 'distance': distance, 'time': time})


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=80)