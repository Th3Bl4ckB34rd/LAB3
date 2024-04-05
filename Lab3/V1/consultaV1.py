import mysql.connector
from flask import Flask, render_template, request, redirect, url_for

# Database configuration
db_config = {
    "host": "localhost",
    "user": "frank4770",
    "password": "mysql9010",
    "database": "vulnerable_app"
}

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(**db_config)

@app.route("/")
def index():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template("index.html", users=users)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Vulnerability: Insecure data storage
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for("index"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Vulnerability: Insecure authentication
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Credenciales incorrectas")
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
