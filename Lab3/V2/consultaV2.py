import mysql.connector
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash  # Password Hashing

# Credentialsstore these securely
db_host = "localhost"
db_user = "frank4770"
db_password = "mysql9010"
db_name = "vulnerable_app"

# Flask
app = Flask(__name__)
app.secret_key = 'v2vulnerable788912'

# Fuction to connect the DB
def get_connection():
    return mysql.connector.connect(
        host=db_host, user=db_user, password=db_password, database=db_name
    )

# Register Route (sanitized and parameterized)
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Escape special characters to prevent XSS (optional for text fields)
        # sanitized_username = quote(username)
        # sanitized_email = quote(email)

        # Hashing password before storing
        hashed_password = generate_password_hash(password)

        # Parametrized query for secure execution
        query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (username, email, hashed_password))
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for("login"))

    return render_template("register.html")

# Login (sanitized and parameterized)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Parametrized query for secure execution
        query = "SELECT * FROM users WHERE username = %s"
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user and check_password_hash(user['password'], password):
            # Successful login (consider using Flask-Login for sessions)
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Usuario o contraseña incorrectos.")

    return render_template("login.html")

# Path to index (consider access control)
@app.route("/")
def index():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("index.html", users=users)

# Path to edit profile (sanitized and parameterized)
@app.route("/edit_profile/<int:user_id>", methods=["GET", "POST"])
def edit_profile(user_id):
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Escape special characters to prevent XSS 
        # sanitized_username = quote
        # sanitized_email = quote

        # Hashing password before storing
        hashed_password = generate_password_hash(password)

        # Parametrized query for secure execution
        query = "UPDATE users SET username = %s, email = %s, password = %s WHERE user_id = %s"
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (username, email, hashed_password, user_id))
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for("index"))

connection = get_connection()
cursor = connection.cursor()
cursor.execute(f"SELECT * FROM users WHERE user_id = %s", (user_id,))  # Use parametrized query
user = cursor.fetchone()
cursor.close()
connection.close()

if user:
    return render_template("edit_profile.html", user=user)
else:
    return render_template("error.html", message="Usuario no encontrado.")  # Handle non-existent user

# Application start
if __name__ == "__main__":
    app.run(debug=True)

    
