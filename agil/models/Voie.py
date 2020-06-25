from agil import db


class Voie(db.Model):
    __tablename__ = 'voie'
    idVoie = db.Column(db.Integer, primary_key=True, nullable=False,autoincrement=True)
    nomVoie = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"Voie('{self.idVoie}', '{self.nomVoie}')"
