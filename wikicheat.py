import time
from web_scraper import checkIfExsits
from fast import degree_distance
from connect_db_test import get_db
from flask import session


def wikicheat(start_link, end_link):
    start_time = time.time()
    path_length = degree_distance(start_link, end_link)
    runtime = round(time.time() - start_time, 3)

    start_time = time.time()
    user_id = session['user_id']
    cursor = get_db()
    cursor.execute("INSERT INTO wikipages (title) VALUES (%s) ON CONFLICT DO NOTHING;", (start_link, ))
    cursor.execute("INSERT INTO wikipages (title) VALUES (%s) ON CONFLICT DO NOTHING;", (end_link,))
    cursor.execute("""INSERT INTO history (user_id, start_link, end_link, degrees_away, runtime) 
                    VALUES (
                        %s,
                        (SELECT wiki_id FROM wikiPages WHERE title=%s),
                        (SELECT wiki_id FROM wikiPages WHERE title=%s),
                        %s,
                        %s
                    );""", (user_id, start_link, end_link, path_length, runtime))

    print("Insert into history runtime: ", round(time.time() - start_time, 3))

    # cursor.execute("SELECT MAX(history_id) FROM history;")        
    # history_id = cursor.fetchall()[0][0]

    # #check all records
    # cursor.execute("SELECT r.type_of_record, h.degrees_away ,h.runtime FROM records r LEFT JOIN history h ON r.history_id = h.history_id;")
    # records = cursor.fetchall()
    # for record in records:
    #     if record[0] == 'longest_runtime' and runtime > record[2]:
    #         cursor.execute("UPDATE records SET history_id={} WHERE type_of_record = '{}';".format(history_id, "longest_runtime"))
    #     if record[0] == 'shortest_runtime' and runtime < record[2]:
    #         cursor.execute("UPDATE records SET history_id={} WHERE type_of_record = '{}';".format(history_id, "shortest_runtime"))
    #     if record[0] == 'longest_path' and path_length > record[1]:
    #         cursor.execute("UPDATE records SET history_id={} WHERE type_of_record = '{}';".format(history_id, "longest_path"))
    #     #Update most recent history
    #     cursor.execute("UPDATE records SET history_id={} WHERE type_of_record = '{}';".format(history_id, "most_recent"))
    cursor.close()

    dataLayer = {"event": "wikicheat", "user_id": user_id}
    # session['user_engagement']['games_played'] += 1
    # session.modified = True

    return path_length, runtime














# if request.method == 'POST':
        # start_link = request.form['start_link'].replace(" ", "_")
        # end_link = request.form['end_link'].replace(" ", "_")

        # if not start_link or not end_link:
        #     return render_template("wikicheat.html", errormessage = "Please enter 2 Valid Values")
        # elif not checkIfExsits(start_link):
        #     return render_template("wikicheat.html", errormessage = "The first link you enterd does not exsits")
        # elif not checkIfExsits(end_link):
        #     return render_template("wikicheat.html", errormessage = "The second link you enterd does not exsits")
        # elif start_link == end_link:
        #     return render_template("wikicheat.html", errormessage = "Please enter two different links")


        # start_time = time.time()
        # path_length = degree_distance(start_link, end_link)
        # runtime = round(time.time() - start_time, 3)

        # user_id = session['user_id']
        # cursor = get_db()
        # cursor.execute("INSERT INTO wikipages (title) VALUES ('{0}') ON CONFLICT DO NOTHING;".format(start_link))
        # cursor.execute("INSERT INTO wikipages (title) VALUES ('{0}') ON CONFLICT DO NOTHING;".format(end_link))
        # cursor.execute("""INSERT INTO history (user_id, start_link, end_link, degrees_away, runtime) 
        #                 VALUES (
        #                     {user_id},
        #                     (SELECT wiki_id FROM wikiPages WHERE title='{start_link}'),
        #                     (SELECT wiki_id FROM wikiPages WHERE title='{end_link}'),
        #                     {degrees_away},
        #                     {runtime}
        #                 );""".format(user_id=user_id, start_link=start_link, end_link=end_link, degrees_away=path_length, runtime=runtime))

        # cursor.execute("SELECT MAX(history_id) FROM history;")        
        # history_id = cursor.fetchall()[0][0]

        # #check all records
        # cursor.execute("SELECT r.type_of_record, h.degrees_away ,h.runtime FROM records r LEFT JOIN history h ON r.history_id = h.history_id;")
        # records = cursor.fetchall()
        # for record in records:
        #     if record[0] == 'longest_runtime' and runtime > record[2]:
        #         cursor.execute("UPDATE records SET history_id={} WHERE type_of_record = '{}';".format(history_id, "longest_runtime"))
        #     if record[0] == 'shortest_runtime' and runtime < record[2]:
        #         cursor.execute("UPDATE records SET history_id={} WHERE type_of_record = '{}';".format(history_id, "shortest_runtime"))
        #     if record[0] == 'longest_path' and path_length > record[1]:
        #         cursor.execute("UPDATE records SET history_id={} WHERE type_of_record = '{}';".format(history_id, "longest_path"))
        #     #Update most recent history
        #     cursor.execute("UPDATE records SET history_id={} WHERE type_of_record = '{}';".format(history_id, "most_recent"))

        # cursor.close()

        # dataLayer = {"event": "wikicheat", "user_id": user_id}
        # session['user_engagement']['games_played'] += 1
        # session.modified = True
        # result = {"start_link": start_link, "end_link": end_link, "path_length": path_length, "runtime": runtime}
        # return render_template("wikicheat.html", result = result, dataLayer=dataLayer)