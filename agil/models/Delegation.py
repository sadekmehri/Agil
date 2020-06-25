from agil import db
from agil.models.Ville import Ville


class Delegation(db.Model):
    __tablename__ = 'delegation'
    idDelegation = db.Column(db.Integer, primary_key=True, nullable=False,autoincrement=True)
    nomDelegation = db.Column(db.String(255), nullable=False)
    idVille = db.Column(db.ForeignKey('ville.idVille'), nullable=False)
    Ville = db.relationship("Ville", backref='Ville', lazy=True)

    def __repr__(self):
        return f"Delegation('{self.idDelegation}', '{self.nomDelegation}', '{self.idVille}')"
