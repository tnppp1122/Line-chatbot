from app import db


class Test(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
