from agil import db
from agil.models.Pompe import Pompe
from agil.models.Citerne import Citerne


class PompeCiterne(db.Model):
    __tablename__ = 'citerne_has_pompe'
    id_citerne_has_pompe = db.Column(db.Integer, primary_key=True, nullable=False,autoincrement=True)
    idCiterne = db.Column(db.ForeignKey('citerne.idCiterne'), nullable=False)
    idPompe = db.Column(db.ForeignKey('pompe.idPompe'), nullable=False)
    Citerne = db.relationship("Citerne", backref='Citerne', lazy=True)
    Pompe = db.relationship("Pompe", backref='Pompe', lazy=True)

    def __repr__(self):
        return f"PompeCiterne('{self.id_citerne_has_pompe}',{self.idCiterne}', '{self.idPompe}') "
