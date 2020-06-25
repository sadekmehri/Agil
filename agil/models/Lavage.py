from agil import db


class Lavage(db.Model):
    __tablename__ = 'lavage'
    idLavage = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    TypeLavage = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"Lavage('{self.idLavage}', '{self.TypeLavage}')"
