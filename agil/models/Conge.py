from agil import db
from agil.Main.utils import currentDate


class Conge(db.Model):
    __tablename__ = 'conge'
    idConge = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    idEmp = db.Column(db.ForeignKey('employee.idEmp'), nullable=False)
    idGroupe = db.Column(db.ForeignKey('groupe.idGroupe'), nullable=False)
    idTypeConge = db.Column(db.ForeignKey('typeconge.idTypeConge'), nullable=False)
    idStation = db.Column(db.ForeignKey('station.idStation'), nullable=False)
    DateDebConge = db.Column(db.Date, nullable=False, default=currentDate)
    DateFinConge = db.Column(db.Date, nullable=False)
    DescConge = db.Column(db.String(255), nullable=False)
    Employee = db.relationship("Employee", backref='Empe', lazy=True)
    Station = db.relationship("Station", backref='Sts', lazy=True)
    TypeConge = db.relationship("TypeConge", backref='TpConge', lazy=True)
    Groupe = db.relationship("Groupe", backref='Grp', lazy=True)

    def __repr__(self):
        return f"Conge('{self.idConge}','{self.DateDebConge}','{self.DateFinConge}','{self.DescConge}','{self.idStation}','{self.idTypeConge}','{self.idEmp}','{self.idGroupe}')"


class TypeConge(db.Model):
    __tablename__ = 'typeconge'
    idTypeConge = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    typeConge = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"TypeConge('{self.idTypeConge}','{self.typeConge}')"

