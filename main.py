from flask import Flask, request, render_template, redirect, make_response

app = Flask(__name__)

users = []

user_data = {}


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        login = request.form.get("login", "")
        password = request.form.get("password", "")
        if login == "" or password == "":
            return "Введите оба поля!!!"
        users.append({"login": login, "password": password})
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
        for user in users:
            if user["login"] == login and user["password"] == password:
                response = make_response(redirect("/"))
                response.set_cookie("login", login)
                return response
        return "Нет такого пользователя"
    else:
        return render_template('login.html')


@app.route("/")
def index():
    login = request.cookies.get("login", "")
    secret = user_data.get(login, "")
    return render_template("index.html", name=login, secret=secret)


@app.route("/add_secret", methods=["POST", "GET"])
def secret():
    login = request.cookies.get("login", "")
    if login == "":
        return "GO AWAY PLS"
    if request.method == "POST":
        secret = request.form.get("secret", "")
        user_data[login] = secret
        return redirect("/")
    else:
        return render_template("secret.html")


app.run()
