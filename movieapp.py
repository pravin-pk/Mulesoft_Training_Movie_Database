from flask import Flask, render_template, redirect, url_for, request
import sqlite3

app = Flask(__name__)


@app.route("/insert" , methods = ['POST', 'GET'])
def insert():
    try:
        conn = sqlite3.connect("movieDB.db")
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO MOVIES(MOVIE, ACTOR, ACTRESS, YEAROFRELEASE, DIRECTOR) VALUES(?, ?, ?, ?, ?)",
            (
                request.form.get("movie"), 
                request.form.get("actor"),
                request.form.get("actress"),
                request.form.get("yearofrelease"),
                request.form.get("director")
            ),
        )
        
        cur.close()
        conn.commit()
        return redirect(url_for("home"))
    except sqlite3.Error  as e:
        print(e)
        return e


@app.route("/", methods = ['POST', 'GET'])
def home():
    if request.method != "POST":
        conn = sqlite3.connect("movieDB.db")
        cur = conn.cursor()

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS MOVIES(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        MOVIE TEXT,
                        ACTOR TEXT,
                        ACTRESS TEXT,
                        YEAROFRELEASE TEXT,
                        DIRECTOR TEXT
                    )
                    """)
        conn.commit()

        cur.execute("SELECT * FROM MOVIES")
        data = cur.fetchall()
        cur.close()

        return render_template("home.html", content = data)

    if request.form.get("queryvalue") == '':
        return redirect(url_for("home"))

    conn = sqlite3.connect("movieDB.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM MOVIES WHERE "+ request.form.get("queryfactor") + " LIKE '%" + request.form.get("queryvalue") + "%';")

    data = cur.fetchall()

    cur.close()

    return render_template("home.html", content = data)
    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
