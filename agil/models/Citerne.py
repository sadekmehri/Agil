from agil import db
from agil.models.Station import Station
from agil.models.Carburant import Carburant


class Citerne(db.Model):
    __tablename__ = 'citerne'
    idCiterne = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    NomCiterne = db.Column(db.String(255), nullable=False)
    VolumeCiterne = db.Column(db.Float, nullable=False)
    Val_Act_Citerne = db.Column(db.Float, nullable=False)
    Min_Val_Citerne = db.Column(db.String(255), nullable=False)
    EtatCiterne = db.Column(db.String(10), nullable=False, default="1")
    idCarburant = db.Column(db.ForeignKey('carburant.idCarburant'), nullable=False)
    idStation = db.Column(db.ForeignKey('station.idStation'), nullable=False)
    Carburant = db.relationship("Carburant", backref='Carburant', lazy=True)
    Station = db.relationship("Station", backref='station', lazy=True)

    def __repr__(self):
        return f"Citerne('{self.idCiterne}', '{self.NomCiterne}', '{self.VolumeCiterne}','{self.Val_Act_Citerne}'," \
               f"'{self.Min_Val_Citerne}', '{self.EtatCiterne}', '{self.idCarburant}', '{self.idStation}') "
