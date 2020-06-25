from agil import db
from agil.Chef.utils import currentDate


class Expenses(db.Model):

    __tablename__ = 'expenses'
    idExpenses = db.Column(db.Integer, primary_key=True, nullable=False,autoincrement=True)
    dateExpenses = db.Column(db.DATE, nullable=False, default=currentDate)
    catExpenses = db.Column(db.String(255), nullable=False)
    descExpenses = db.Column(db.String(255), nullable=False)
    amExpenses = db.Column(db.Float, nullable=False)
    idStation = db.Column(db.ForeignKey('station.idStation'), nullable=False)
    Station = db.relationship("Station", backref='Stattion', lazy=True)

    def __repr__(self):
        return f"Expenses('{self.idExpenses}', '{self.dateExpenses}','{self.catExpenses}', '{self.descExpenses}', '{self.amExpenses}', '{self.idStation}')"
