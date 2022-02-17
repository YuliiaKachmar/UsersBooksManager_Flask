from auth import JWToken
from flask_restful import Resource, abort
from flask import request, jsonify, session, Blueprint, url_for, render_template, make_response

from db import db
from Schemas.user_schema import users_schema, user_schema
from Models.user import User
from oauth import oauth


blueprint = Blueprint('blueprint', __name__, )


class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        summary_schema = users_schema("name", "surname", "email", "country")
        return summary_schema.dump(users)


class LogInUser(Resource):
    def get(self):
        return make_response(render_template('login.html'))

    def post(self):
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return {
                       "message": "Check your input",
                       "data": None,
                       "error": "Unauthorized access"
                   }, 401
        token = JWToken.encode_token(user, "random string")
        return jsonify({'token': token})


class UserRegistration(Resource):
    def get(self):
        return make_response(render_template('registration.html'))

    def post(self):
        name = request.form.get('name')
        surname = request.form.get('surname')
        email = request.form.get('email')
        country = request.form.get('country')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        if not password == password_confirm:
            abort(400, message='Passwords must be equal')
        elif not email or not password:
            abort(400, message='missing argument')
        elif User.query.filter_by(email=email).first():
            abort(400, message='existing user')
        else:
            new_user = User(name, surname, email, country, False)
            new_user.set_password(password)

            db.session.add(new_user)
            db.session.commit()

        return user_schema.dump(new_user)


class UserGoogleLogIn(Resource):
    def get(self):
        google = oauth.create_client('google')
        redirect_uri = url_for('blueprint.authorize', _external=True)
        return google.authorize_redirect(redirect_uri)


@blueprint.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    user = oauth.google.userinfo()
    session['profile'] = user_info
    session.permanent = True
    email = dict(session)['profile']['email']
    user_current = User.query.filter_by(email=email).first()
    if not user_current:
        return {
                   "message": "No such user",
                   "data": None,
                   "error": "Unauthorized access"
               }, 401
    token = JWToken.encode_token(user_current, "random string")
    return jsonify({'token': token})


class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user_schema.dump(user)

    def patch(self, user_id):
        user = User.query.get_or_404(user_id)

        if 'name' in request.json:
            user.name = request.json['name']
        if 'surname' in request.json:
            user.surname = request.json['surname']
        if 'email' in request.json:
            user.email = request.json['email']
        if 'country' in request.json:
            user.country = request.json['country']

        db.session.commit()
        return user_schema.dump(user)

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204
