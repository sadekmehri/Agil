from agil import db


class Role(db.Model):
    __tablename__ = 'role'
    idRole = db.Column(db.Integer, primary_key=True, nullable=False,autoincrement=True)
    NomRole = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"Role('{self.idRole}', '{self.NomRole}')"
