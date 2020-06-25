from agil import db
from sqlalchemy.dialects.mysql import TINYINT
from agil.Chef.utils import currentDate


class ToDo(db.Model):
    __tablename__ = 'listuser'
    idListUser = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    objListUser = db.Column(db.String(255), nullable=False, unique=True)
    dateListUser = db.Column(db.Date, nullable=False, default=currentDate)
    stateListUser = db.Column(TINYINT, nullable=False, default=1)
    delListUser = db.Column(TINYINT, nullable=False, default=1)
    idUser = db.Column(db.ForeignKey('user.idUser'), nullable=False)
    User = db.relationship("User", backref='UserList', lazy=True)

    def __repr__(self):
        return f"ToDo('{self.idListUser}', '{self.objListUser}' ,'{self.dateListUser}', '{self.stateListUser}'," \
               f" '{self.delListUser}','{self.idUser}')"
