from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"



def create_app():
    app = Flask(__name__)

    from .views import views
    app.register_blueprint(views)

    from. info import info
    app.register_blueprint(info)


    from .auth import auth
    app.register_blueprint(auth)

    from .quiz import quiz
    app.register_blueprint(quiz)

    from .pexeso import pexeso
    app.register_blueprint(pexeso)

    from .memory_game import memory
    app.register_blueprint(memory)




    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .model import User 

    with app.app_context():
        create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all()
        print('Created Database!')

