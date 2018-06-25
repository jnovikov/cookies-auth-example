from flask import Flask, request, render_template, redirect, make_response
import sqlite3

conn = sqlite3.connect("test.db")

db = conn.cursor()

app = Flask(__name__)


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        login = request.form.get("login", "")
        password = request.form.get("password", "")
        if login == "" or password == "":
            return "Введите оба поля!!!"

        add_new = "INSERT INTO users (login, password) VALUES ('{}','{}')".format(login, password)
        db.execute(add_new)
        conn.commit()
        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        login = request.form.get("login", "")
        password = request.form.get("password", "")
        if login == "" or password == "":
            return "Введите оба поля!!!"

        find_user = "SELECT * FROM users WHERE login = '{}' AND password = '{}'".format(login, password)

        db.execute(find_user)

        user = db.fetchone()

        if user is not None:
            response = make_response(redirect("/"))
            response.set_cookie("id", str(user[0]))
            return response
        return "Нет такого пользователя"
    else:
        return render_template('login.html')


@app.route("/")
def index():
    id = request.cookies.get("id", "-1")

    find_secret = "SELECT text FROM secrets WHERE user_id = {}".format(id)
    db.execute(find_secret)
    secret = db.fetchone()
    if secret:
        secret = secret[0]
    else:
        secret = "Empty"

    user_name = "SELECT login FROM users WHERE id = {}".format(id)
    db.execute(user_name)
    login = db.fetchone()

    if login:
        login = login[0]
    else:
        login = "Anon"


    return render_template("index.html", name=login, secret=secret)


@app.route("/add_secret", methods=["POST", "GET"])
def secret():
    id = request.cookies.get("id", "")
    if id == "":
        return "GO AWAY PLS"
    if request.method == "POST":
        secret = request.form.get("secret", "")
        insert_secret = "INSERT INTO secrets (text, user_id) VALUES ('{}',{})".format(secret, id)
        db.execute(insert_secret)
        conn.commit()
        return redirect("/")
    else:
        return render_template("secret.html")


create_users_table = "CREATE TABLE IF NOT EXISTS users " \
                     "(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT," \
                     "login VARCHAR(200), password VARCHAR(200))"

create_secret_table = "CREATE TABLE IF NOT EXISTS secrets " \
                      "(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT," \
                      "text VARCHAR(500), user_id INTEGER)"

db.execute(create_users_table)
db.execute(create_secret_table)
conn.commit()

app.run()
