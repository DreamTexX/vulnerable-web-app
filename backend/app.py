import json
from flask import Flask, request, session, Response
import mariadb
import sys
import re
from os import environ
from argon2 import PasswordHasher

try:
    conn: mariadb.Connection = mariadb.connect(
        user=environ.get("DB_USER"),
        password=environ.get("DB_PASSWORD"),
        host=environ.get("DB_HOST"),
        port=3306,
        database=environ.get("DB_NAME")
    )
except mariadb.Error as e:
    print(f"Error connecting to MySQL Platform: {e}")
    sys.exit(1)

hasher = PasswordHasher()

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = "super-secret"


@app.route("/api/auth/login", methods=["POST"])
def api_login():
    pass


@app.route("/api/auth/register", methods=["POST"])
def api_register():
    # Extract data from request body
    data = request.get_json()

    # Check if this e-mail is already in use
    cur = conn.cursor()
    cur.execute(
        f"""SELECT `email` FROM `accounts` WHERE `email` LIKE '{data["email"]}';""")

    if cur.rowcount > 0:
        return Response(response=json.dumps({"error": "already-in-use"}), content_type="application/json", status=400)

    # Validate an parse request data
    email = data["email"]
    if not re.search(r'^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$', email):
        return Response(response=json.dumps({"error": "invalid-email"}), content_type="application/json", status=400)

    password = hasher.hash(data["password"])

    # Store user in database
    cur.execute(
        f"""INSERT INTO `accounts` (`email`, `password`) VALUES ('{email}', '{password}');""")
    conn.commit()

    session["id"] = cur.lastrowid

    return {
        "id": cur.lastrowid,
        "email": email,
    }


@app.route("/api/posts", methods=["GET"])
def api_get_all_posts():
    cur = conn.cursor()
    cur.execute(f"""SELECT `id`, `content`, `author_id` FROM `posts`;""")

    headers = ["id", "content", "author_id"]
    rows = cur.fetchall()
    return [dict(zip(headers, row)) for row in rows]


@app.route("/api/posts", methods=["POST"])
def api_create_post():
    if session.get("id") is None:
        return Response(status=403, content_type="application/json", response=json.dumps({"error": "unauthorized"}))

    data = request.get_json()
    content = data["content"]
    author_id = session["id"]

    cur = conn.cursor()
    cur.execute(f"""INSERT INTO `posts` (`content`, `author_id`) VALUES ('{content}', '{author_id}');""")
    conn.commit()

    return {
        "id": cur.lastrowid,
        "content": content,
        "author_id": author_id,
    }


if __name__ == "__main__":
    app.run()
