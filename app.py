from datetime import timedelta
from dotenv import load_dotenv

from flask import Flask
from ma import ma
from api import api, blueprint
from db import db
from oauth import oauth

load_dotenv()


def create_app():
    app = Flask(__name__, template_folder="template")

    app.register_blueprint(blueprint)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users_books_DB.sqlite3'
    app.config['SECRET_KEY'] = "random string"
    app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

    db.init_app(app)
    api.init_app(app)
    ma.init_app(app)
    oauth.init_app(app)

    google = oauth.register(
        name='google',
        client_id="868951780418-3bi86n5ctkv3dohb0647ivmo0pcc1ui7.apps.googleusercontent.com",
        client_secret="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",
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
        client_kwargs={'scope': 'openid email profile'},
    )

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run( debug=True)