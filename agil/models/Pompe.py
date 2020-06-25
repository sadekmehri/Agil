from agil import db


class Pompe(db.Model):
    __tablename__ = 'pompe'
    idPompe = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    NomPompe = db.Column(db.String(255), nullable=False)
    EtatPompe = db.Column(db.String(10), nullable=False, default="1")
    idStation = db.Column(db.ForeignKey('station.idStation'), nullable=False)
    Station = db.relationship("Station", backref='Stations', lazy=True)

    def __repr__(self):
        return f"Pompe('{self.idPompe}', '{self.NomPompe}', '{self.EtatPompe}','{self.idStation}') "
