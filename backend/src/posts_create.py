from flask import Blueprint, request, session
from db import pool

posts_create_blueprint = Blueprint('posts_create', __name__)


@posts_create_blueprint.route("/api/posts", methods=["POST"])
def api_create_post():
    if session.get("id") is None:
        return {"error": "unauthorized"}, 403

    data = request.get_json()
    content = data["content"]
    author_id = session["id"]

    conn = pool.get_connection()
    cur = conn.cursor(dictionary=True, buffered=True)
    cur.execute(
        f"""INSERT INTO `posts` (`content`, `author_id`) VALUES ('{content}', '{author_id}');""")
    conn.commit()
    cur.execute(
        f"""SELECT `posts`.`id`, `posts`.`content`, `accounts`.`username`, `posts`.`created_at` FROM `posts` INNER JOIN `accounts` ON `accounts`.`id` = `posts`.`author_id` WHERE `posts`.`id` = {cur.lastrowid}""")
    data = cur.fetchone()
    conn.close()

    return data, 201
