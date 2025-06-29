from flask import Flask
from flask_migrate import Migrate
from models import db, bcrypt
from resources import Signup, CheckSession, Login, Logout, RecipeIndex
import config

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    bcrypt.init_app(app)
    migrate = Migrate(app, db)

    from flask_restful import Api
    api = Api(app)
    api.add_resource(Signup, '/signup')
    api.add_resource(CheckSession, '/check_session')
    api.add_resource(Login, '/login')
    api.add_resource(Logout, '/logout')
    api.add_resource(RecipeIndex, '/recipes')

    return app

if __name__ == '__main__':
    create_app().run(debug=True)

app = create_app()
