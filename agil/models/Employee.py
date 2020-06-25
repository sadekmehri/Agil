from agil import db


class Employee(db.Model):
    __tablename__ = 'employee'
    idEmp = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    codeEmp = db.Column(db.String(255), nullable=False, unique=True)
    cinEmp = db.Column(db.String(255), nullable=False)
    nomEmp = db.Column(db.String(255), nullable=False)
    prenomEmp = db.Column(db.String(255), nullable=False)
    dateEmp = db.Column(db.DATE, nullable=False)
    telEmp = db.Column(db.String(255), nullable=False)
    salEmp = db.Column(db.Float, nullable=False)
    idGroupe = db.Column(db.ForeignKey('groupe.idGroupe'), nullable=False)
    idRole = db.Column(db.ForeignKey('role.idRole'), nullable=False)
    idStation = db.Column(db.ForeignKey('station.idStation'), nullable=False)
    Role = db.relationship("Role", backref='Role', lazy=True)
    Station = db.relationship("Station", backref='Statn', lazy=True)
    Groupe = db.relationship("Groupe", backref='Group', lazy=True)

    def __repr__(self):
        return f"Employee('{self.idEmp}', '{self.codeEmp}' ,'{self.cinEmp}', '{self.nomEmp}', '{self.prenomEmp}', " \
               f"'{self.dateEmp}','{self.telEmp}','{self.salEmp}','{self.idRole}','{self.idStation}')"