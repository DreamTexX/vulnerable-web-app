from flask import Flask
from auth_register import auth_register_blueprint
from auth_login import auth_login_blueprint
from auth_logout import auth_logout_blueprint
from posts_create import posts_create_blueprint
from posts_list import posts_list_blueprint
from accounts_me import accounts_me_blueprint

app = Flask(__name__)
app.secret_key = "super-secret"
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.register_blueprint(auth_register_blueprint)
app.register_blueprint(auth_login_blueprint)
app.register_blueprint(auth_logout_blueprint)
app.register_blueprint(posts_create_blueprint)
app.register_blueprint(posts_list_blueprint)
app.register_blueprint(accounts_me_blueprint)

if __name__ == "__main__":
    app.run()
