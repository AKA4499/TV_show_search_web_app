'''
This file will make web_app folder a python package
'''
from flask import Flask
#package for database handling in python
from flask_sqlalchemy import SQLAlchemy   
from os import path
# login  management
from flask_login import LoginManager  

#databse object defined
db = SQLAlchemy()
DB_NAME = "database.db"  


def create_app():
    #flask app initialised
    app = Flask(__name__)
    #app requires a secret key which secures the cookies related to website data
    app.config['SECRET_KEY'] = 'jhfbiarfonkl'
    #database url
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # initialising the database
    db.init_app(app)
    

    # importing all the url and blueprints defined in different files
    from .views import views
    from .auth import auth


    #register all the routes with / as url prefix 
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # define all our classes before actually creating the database
    from .models import User, Show, Cast, Crew, Date 

    # create the database with all the classes defined
    create_database(app)

    # object of login manager
    login_manager = LoginManager()
    # if the user is not logged it go to login page
    login_manager.login_view = 'auth.login'
    # initialise login manager in the flask app
    login_manager.init_app(app)

    # for loading user based on id 
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

#func for creating database
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
