from flask import Blueprint
from db import pool

posts_list_blueprint = Blueprint('posts_list', __name__)


@posts_list_blueprint.route("/api/posts", methods=["GET"])
def api_get_all_posts():
    conn = pool.get_connection()
    cur = conn.cursor(dictionary=True, buffered=True)
    cur.execute(f"""SELECT `posts`.`id`, `posts`.`content`, `accounts`.`username`, `posts`.`created_at` FROM `posts` INNER JOIN `accounts` ON `accounts`.`id` = `posts`.`author_id` ORDER BY `posts`.`created_at` DESC;""")
    data = cur.fetchall()
    conn.close()

    return data, 200