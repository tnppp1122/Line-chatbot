from app import db

class Leave(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String())
    total_leave = db.Column(db.Integer())
    leave = db.Column(db.Integer())
    
