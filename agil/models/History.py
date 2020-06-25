from sqlalchemy.dialects.mysql import TINYINT
from agil.Chef.utils import currentDateTime
from agil import db


class LogUser(db.Model):
    __tablename__ = 'loguser'
    idLoginHist = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    srcIp = db.Column(db.String(255), nullable=False)
    dateAttempt = db.Column(db.String(255), nullable=False, default=currentDateTime)
    statusAttempt = db.Column(TINYINT, nullable=False)
    descAttempt = db.Column(db.String(255), nullable=False)
    idUser = db.Column(db.ForeignKey('user.idUser'), nullable=False)
    User = db.relationship("User", backref='User', lazy=True)

    def __repr__(self):
        return f"LogIn('{self.idLoginHist}', '{self.srcIp}' , '{self.dateAttempt}','{self.statusAttempt}','{self.descAttempt}','{self.idUser}')"
