from agil import db
from sqlalchemy.dialects.mysql import TINYINT


class Comment(db.Model):

    def currentDateTime(self):
        import datetime
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True, nullable=False,autoincrement=True)
    comment_subject = db.Column(db.String(255), nullable=False)
    comment_date = db.Column(db.String(255), nullable=False,default=currentDateTime)
    comment_text = db.Column(db.String(255), nullable=False)
    comment_status = db.Column(TINYINT, nullable=False,default=1)
    idUser = db.Column(db.ForeignKey('user.idUser'), nullable=False)
    User = db.relationship("User", backref='Users', lazy=True)

    def __repr__(self):
        return f"Comment('{self.comment_id}', '{self.comment_subject}', '{self.comment_date}', '{self.comment_text}','{self.comment_status}','{self.idUser}')"
