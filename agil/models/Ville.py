from agil import db


class Ville(db.Model):
    __tablename__ = 'ville'
    idVille = db.Column(db.Integer, primary_key=True, nullable=False,autoincrement=True)
    NomVille = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"Ville('{self.idVille}', '{self.NomVille}')"
