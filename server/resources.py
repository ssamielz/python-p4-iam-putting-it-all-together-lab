from flask import request, session
from flask_restful import Resource
from models import db, User, Recipe

def format_user(u):
    return {"id": u.id, "username": u.username, "image_url": u.image_url, "bio": u.bio}

class Signup(Resource):
    def post(self):
        data = request.get_json()
        try:
            u = User(username=data['username'], image_url=data.get('image_url'), bio=data.get('bio'))
            u.password_hash = data['password']
            db.session.add(u)
            db.session.commit()
            session['user_id'] = u.id
            return format_user(u), 201
        except Exception as e:
            db.session.rollback()
            errors = []
            for error in e.args:
                errors.append(str(error))
            return {"errors": errors}, 422

class CheckSession(Resource):
    def get(self):
        uid = session.get('user_id')
        if not uid:
            return {"errors": ["Unauthorized"]}, 401
        u = User.query.get(uid)
        return format_user(u), 200

class Login(Resource):
    def post(self):
        data = request.get_json()
        u = User.query.filter_by(username=data['username']).first()
        if u and u.authenticate(data['password']):
            session['user_id'] = u.id
            return format_user(u), 200
        return {"errors": ["Invalid credentials"]}, 401

class Logout(Resource):
    def delete(self):
        if 'user_id' not in session:
            return {"errors": ["Unauthorized"]}, 401
        session.pop('user_id')
        return '', 204

class RecipeIndex(Resource):
    def get(self):
        uid = session.get('user_id')
        if not uid:
            return {"errors": ["Unauthorized"]}, 401
        recs = Recipe.query.all()
        return [{"id": r.id, "title": r.title, "instructions": r.instructions,
            "minutes_to_complete": r.minutes_to_complete,
            "user": format_user(r.user)} for r in recs], 200

    def post(self):
        uid = session.get('user_id')
        if not uid:
            return {"errors": ["Unauthorized"]}, 401
        data = request.get_json()
        try:
            r = Recipe(title=data['title'], instructions=data['instructions'],
                       minutes_to_complete=data['minutes_to_complete'], user_id=uid)
            db.session.add(r)
            db.session.commit()
            return {"id": r.id, "title": r.title, "instructions": r.instructions,
                    "minutes_to_complete": r.minutes_to_complete,
                    "user": format_user(r.user)}, 201
        except Exception as e:
            db.session.rollback()
            return {"errors": [str(e)]}, 422
