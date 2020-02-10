from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager
import yaml

db = SQLAlchemy()
def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)


def create_app():
    app = Flask(__name__)

    POSTGRES_URL = get_env_variable("POSTGRES_URL")
    POSTGRES_USER = get_env_variable("POSTGRES_USER")
    POSTGRES_PASS = get_env_variable("POSTGRES_PASS")
    POSTGRES_DB = get_env_variable("POSTGRES_DB")

    DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PASS,url=POSTGRES_URL,db=POSTGRES_DB)

    app.config['SECRET_KEY'] = '843awf09n09aw93485a0dfpq'
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    migrate = Migrate(app, db)
    manager = Manager(app)

    from .models import User, Role, UserRoles
    admin_role = Role(name ='Admin')
    instructor_role = Role(name='Instructor')
    student_role = Role(name='Student')
    db.init_app(app)

    #admin = User(username='jack', email='admin@fake.com', password=

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

