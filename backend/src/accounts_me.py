from flask import Blueprint, session
from db import pool

accounts_me_blueprint = Blueprint('accounts_me', __name__)


@accounts_me_blueprint.route("/api/accounts/@me", methods=["GET"])
def get_account_own():
    if session.get("id") is None:
        return {"error": "unauthorized"}, 403

    conn = pool.get_connection()
    cur = conn.cursor(dictionary=True, buffered=True)
    cur.execute(
        f"""SELECT `id`, `email`, `username` FROM `accounts` WHERE `id` = {session["id"]}""")
    if cur.rowcount == 0:
        session.clear()
        conn.close()
        return {"error": "not-found"}, 404

    data = cur.fetchone()
    conn.close()
    return data, 200
