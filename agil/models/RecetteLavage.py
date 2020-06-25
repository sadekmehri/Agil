from agil import db
from agil.Chef.utils import currentDate
from agil.models.Station import Station
from agil.models.Ville import Ville


class RecetteLavage(db.Model):

    __tablename__ = 'recettelavage'
    idRecetteLavage = db.Column(db.Integer, primary_key=True, nullable=False,autoincrement=True)
    MatriculeVoiture = db.Column(db.String(255), nullable=False)
    Kilometrage = db.Column(db.String(255), nullable=False)
    HeureDebut = db.Column(db.String(255), nullable=False)
    HeureFin = db.Column(db.String(255), nullable=False)
    DateLavage = db.Column(db.DATE, nullable=False, default=currentDate)
    PrixLavage = db.Column(db.Float, nullable=False)
    idLavage = db.Column(db.ForeignKey('lavage.idLavage'), nullable=False)
    idGroupe = db.Column(db.ForeignKey('groupe.idGroupe'), nullable=False)
    idStation = db.Column(db.ForeignKey('station.idStation'), nullable=False)
    Lavage = db.relationship("Lavage", backref='Lavage', lazy=True)
    Groupe = db.relationship("Groupe", backref='Groupe', lazy=True)
    Station = db.relationship("Station", backref='Station', lazy=True)

    def __repr__(self):
        return f"RecetteLavage('{self.idRecetteLavage}', '{self.MatriculeVoiture}', " \
               f"'{self.Kilometrage}', '{self.HeureDebut}', '{self.HeureFin}', '{self.DateLavage}'," \
               f"'{self.idLavage}','{self.idGroupe}','{self.idStation}') "
