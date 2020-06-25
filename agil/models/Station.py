from agil import db
from agil.models.Delegation import Delegation


class Station(db.Model):
    __tablename__ = 'station'
    idStation = db.Column(db.Integer, primary_key=True, nullable=False,autoincrement=True)
    NomStation = db.Column(db.String(255), nullable=False)
    AdrStation = db.Column(db.String(255), nullable=False)
    idDelegation = db.Column(db.ForeignKey('delegation.idDelegation'), nullable=False)
    Delegation = db.relationship("Delegation", backref='Delegation', lazy=True)

    def __repr__(self):
        return f"Station('{self.idStation}','{self.NomStation}', '{self.AdrStation}', '{self.idDelegation}')"
