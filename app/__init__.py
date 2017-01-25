# -*- coding: utf-8 -*-

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from config import config

db = SQLAlchemy()
migrate = Migrate()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    migrate.init_app(app, db=db)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .phrases import phrases as phrases_blueprint
    app.register_blueprint(phrases_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    from .utils import utils as utils_blueprint
    app.register_blueprint(utils_blueprint)

    # Initialise flask-admin
    admin = Admin(app, name='ingenuity', template_mode='bootstrap3')
    from app.models import User, PhraseList, Phrase, LatinPhrase, EnglishPhrase

    # Add administrative views here
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(PhraseList, db.session))
    admin.add_view(ModelView(Phrase, db.session))
    admin.add_view(ModelView(LatinPhrase, db.session))
    admin.add_view(ModelView(EnglishPhrase, db.session))

    return app