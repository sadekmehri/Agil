import datetime
import os


class Config:
    SECRET_KEY = os.urandom(50)
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=20)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/agil'  # mysql
    """
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    """
