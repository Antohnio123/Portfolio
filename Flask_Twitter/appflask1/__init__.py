from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from appflask1 import routers, models


# to run a flask server we need being in a app directory run in terminal
# 'set FLASK_APP=hello.py'
# after this 'flask run' will start an app
# To create a db after importing SQLAlchemy and Migrate - run 'flask db init'
# To make migrations of our db: 'flask db migrate -m "Any Name of migration"'
# To use this migration: 'flask db upgrade'