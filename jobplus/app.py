from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from .config import configs
from .models import db, User


def reg_bps(app):
    from .handlers import front, admin, user, job, company
    app.register_blueprint(front)
    app.register_blueprint(admin)
    app.register_blueprint(user)
    app.register_blueprint(job)
    app.register_blueprint(company)


def reg_exts(app):

    db.init_app(app)
    Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(id)

    login_manager.login_view = 'front.login'


def create_app(config):

    app = Flask(__name__)
    app.config.from_object(configs.get(config))

    reg_exts(app)
    reg_bps(app)

    return app