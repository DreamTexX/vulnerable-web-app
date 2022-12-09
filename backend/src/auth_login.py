from flask import Blueprint, request, session
import hashlib
from db import pool

auth_login_blueprint = Blueprint('auth_login', __name__)


@auth_login_blueprint.route("/api/auth/login", methods=["POST"])
def api_login():
    data = request.get_json()
    email = data["email"]
    password = hashlib.sha256(data["password"].encode()).hexdigest()

    try:
        conn = pool.get_connection()
        cur = conn.cursor(buffered=True)
        cur.execute(
            f"""SELECT `id` FROM `accounts` WHERE `email` LIKE '{email}' AND `password` LIKE '{password}';""")

        if cur.rowcount == 0:
            return {"error": "The credentials provided do not match"}, 401

        row = cur.fetchone()
        session["id"] = row[0]
        return {}, 201
    finally:
        cur.close()
        conn.close()
    

