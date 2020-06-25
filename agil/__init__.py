from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from itsdangerous import URLSafeTimedSerializer
from agil.config import Config

mail = Mail()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
ts = URLSafeTimedSerializer(Config.SECRET_KEY)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from agil.Error.routes import error
    from agil.Chef.routes import chef
    from agil.Administrateur.routes import admin
    from agil.Main.routes import approot

    app.register_blueprint(chef)
    app.register_blueprint(admin)
    app.register_blueprint(approot)
    app.register_blueprint(error)

    return app
