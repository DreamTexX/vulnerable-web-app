from flask import Blueprint, session
import hashlib
from db import pool

auth_logout_blueprint = Blueprint('auth_logout', __name__)


@auth_logout_blueprint.route("/api/auth/logout", methods=["DELETE"])
def api_login():
    session.clear()

    return {}, 204