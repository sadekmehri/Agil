from agil import db
from agil.Main.utils import currentDate


class Absence(db.Model):
    __tablename__ = 'absence'
    idAbsence = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    idEmp = db.Column(db.ForeignKey('employee.idEmp'), nullable=False)
    idGroupe = db.Column(db.ForeignKey('groupe.idGroupe'), nullable=False)
    idStation = db.Column(db.ForeignKey('station.idStation'), nullable=False)
    DateAbsence = db.Column(db.Date, nullable=False, default=currentDate)
    DescAbsence = db.Column(db.String(255), nullable=False)
    Employee = db.relationship("Employee", backref='Employee', lazy=True)
    Station = db.relationship("Station", backref='Stationns', lazy=True)
    Groupe = db.relationship("Groupe", backref='Gp', lazy=True)

    def __repr__(self):
        return f"Absence('{self.idAbsence}','{self.DateAbsence}','{self.DescAbsence}','{self.idStation}','{self.idEmp}','{self.idGroupe}')"

