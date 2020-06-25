from agil import db
from agil.Chef.utils import currentDate
from agil.models.Citerne import Citerne


class RecetteCarburant(db.Model):

    __tablename__ = 'recettecarburant'
    idRecetteCarburant = db.Column(db.Integer, primary_key=True, nullable=False,autoincrement=True)
    idPompe = db.Column(db.ForeignKey('pompe.idPompe'), nullable=False)
    idCiterne = db.Column(db.ForeignKey('citerne.idCiterne'), nullable=False)
    idVoie = db.Column(db.ForeignKey('voie.idVoie'), nullable=False)
    idStation = db.Column(db.ForeignKey('station.idStation'), nullable=False)
    idGroupe = db.Column(db.ForeignKey('groupe.idGroupe'), nullable=False)
    DateCarb = db.Column(db.DATE, nullable=False, default=currentDate)
    indiceDeb = db.Column(db.Float, nullable=False)
    indiceFin = db.Column(db.Float, nullable=False)
    prixLitre = db.Column(db.Float, nullable=False)
    Pompe = db.relationship("Pompe", backref='Pmp', lazy=True)
    Citerne = db.relationship("Citerne", backref='Cit', lazy=True)
    Voie = db.relationship("Voie", backref='voie', lazy=True)
    Station = db.relationship("Station", backref='St', lazy=True)
    Groupe = db.relationship("Groupe", backref='Grpp', lazy=True)

    def __repr__(self):
        return f"RecetteCarburant('{self.idRecetteCarburant}', '{self.idPompe}', '{self.idCiterne}','{self.idVoie}'," \
               f"'{self.idStation}', '{self.idGroupe}', '{self.DateCarb}', '{self.indiceDeb}', '{self.indiceFin}') "
