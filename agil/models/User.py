from flask_login import UserMixin
from sqlalchemy.dialects.mysql import TINYINT
from agil import db


class User(db.Model, UserMixin):

    def defaultPass(self):
        return f'$2b$12$VILP2t3.JdQzbSx4qZ7jn.8dzueDJYjx12pJMoj/4ORyFRzPHkFY6'

    # Current Date
    def currentDate(self):
        import datetime
        return datetime.datetime.now().strftime("%Y-%m-%d")

    __tablename__ = 'user'
    idUser = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    codeUser = db.Column(db.String(255), nullable=False, unique=True)
    roleUser = db.Column(TINYINT, nullable=False, default=0)
    cinUser = db.Column(db.String(255), nullable=False, unique=True)
    emailUser = db.Column(db.String(255), nullable=False, unique=True)
    nomUser = db.Column(db.String(255), nullable=False)
    prenomUser = db.Column(db.String(255), nullable=False)
    dateUser = db.Column(db.DATE, nullable=False)
    telUser = db.Column(db.String(255), nullable=False, unique=True)
    passUser = db.Column(db.String(255), nullable=False, default=defaultPass)
    resetTokenUser = db.Column(db.String(255), nullable=False, default='0')
    createCompte = db.Column(db.DATE, nullable=False, default=currentDate)
    expiryCompte = db.Column(db.DATE, nullable=False)
    nbrAttempts = db.Column(db.Integer, nullable=False, default=3)
    etatCompte = db.Column(TINYINT, nullable=False, default=1)
    idStation = db.Column(db.ForeignKey('station.idStation'), nullable=False)
    Station = db.relationship("Station", backref='Stat', lazy=True)

    def get_id(self):
        return self.idUser

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __repr__(self):
        return f"User('{self.idUser}', '{self.codeUser}' ,'{self.roleUser}', '{self.cinUser}','{self.emailUser}'," \
               f"'{self.nomUser}','{self.prenomUser}','{self.dateUser}','{self.telUser}','{self.passUser}'," \
               f"'{self.resetTokenUser}','{self.createCompte}','{self.expiryCompte}','{self.nbrAttempts}','{self.etatCompte}','{self.idStation}')"
