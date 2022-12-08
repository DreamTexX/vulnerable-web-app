import json
from flask import Flask, request, session, Response
import mariadb
import sys
from os import environ
import hashlib

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

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = "super-secret"


@app.route("/api/auth/login", methods=["POST"])
def api_login():
    data = request.get_json()
    email = data["email"]
    password = hashlib.sha256(data["password"].encode()).hexdigest()

    cur = conn.cursor()
    cur.execute(
        f"""SELECT `id`, `password` FROM `accounts` WHERE `email` LIKE '{email}' AND `password` LIKE '{password}';""")

    if cur.rowcount == 0:
        return Response(response=json.dumps({"error": "wrong-credentials"}), content_type="application/json", status=401)

    row = cur.fetchone()
    
    session["id"] = row[0]
    return Response(status=201)


@app.route("/api/auth/register", methods=["POST"])
def api_register():
    # Extract data from request body
    data = request.get_json()
    
    # Validate an parse request data
    email = data["email"]
    password = hashlib.sha256(data["password"].encode()).hexdigest()

    # Check if this e-mail is already in use
    cur = conn.cursor()
    cur.execute(
        f"""SELECT `email` FROM `accounts` WHERE `email` LIKE '{email}';""")

    if cur.rowcount > 0:
        return Response(response=json.dumps({"error": "already-in-use"}), content_type="application/json", status=400)

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
    cur = conn.cursor(dictionary=True)
    cur.execute(f"""SELECT `id`, `content`, `author_id` FROM `posts`;""")

    return cur.fetchall()


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


@app.route("/api/accounts/@me", methods=["GET"])
def get_account_own():
    if session.get("id") is None:
        return Response(status=403, content_type="application/json", response=json.dumps({"error": "unauthorized"}))
    
    cur = conn.cursor()
    cur.execute(f"""SELECT `id`, `email` FROM `accounts` WHERE `id` = {session["id"]}""")
    if cur.rowcount == 0:
        session.clear()
        return Response(status=404, content_type="application/json", response=json.dumps({"error": "not-found"}))

    data = cur.fetchone()
    return {
        "id": data[0],
        "email": data[1]
    }


if __name__ == "__main__":
    app.run()
