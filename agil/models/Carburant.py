from agil import db


class Carburant(db.Model):
    __tablename__ = 'carburant'
    idCarburant = db.Column(db.Integer, primary_key=True, nullable=False,autoincrement=True)
    NomCarburant = db.Column(db.String(255), nullable=False)
    PrixCarburant = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"RecetteLavage('{self.idCarburant}', '{self.NomCarburant} ,'{self.PrixCarburant}') "
