from flask import Blueprint, request, session
import hashlib
from db import pool

auth_register_blueprint = Blueprint('auth_register', __name__)


@auth_register_blueprint.route("/api/auth/register", methods=["POST"])
def api_register():
    # Extract data from request body
    data = request.get_json()

    # parse request data
    email = data["email"]
    username = data["username"]
    password = hashlib.sha256(data["password"].encode()).hexdigest()

    # validate request data
    if email == "" or username == "" or len(data["password"]) < 4:
        return {"error": "invalid-input"}, 400

    # Check if this e-mail/username is already in use
    conn = pool.get_connection()
    cur = conn.cursor(buffered=True)
    cur.execute(
        f"""SELECT `email`, `username` FROM `accounts` WHERE `email` LIKE '{email}' OR `username` LIKE '{username}';""")

    if cur.rowcount > 0:
        conn.close()
        return {"error": "already-in-use"}, 400

    # Store user in database
    cur.execute(
        f"""INSERT INTO `accounts` (`email`, `username`, `password`) VALUES ('{email}', '{username}', '{password}');""")
    conn.commit()
    conn.close()

    # Create session for user
    session["id"] = cur.lastrowid

    return {}, 201
