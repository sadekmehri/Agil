from agil import db


class Groupe(db.Model):
    __tablename__ = 'groupe'
    idGroupe = db.Column(db.Integer, primary_key=True, nullable=False,autoincrement=True)
    NomGroupe = db.Column(db.String(255), nullable=False)
    HeureDebut = db.Column(db.String(255), nullable=False)
    HeureFin = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"Groupe('{self.idGroupe}', '{self.NomGroupe}', '{self.HeureDebut}', '{self.HeureFin}')"
