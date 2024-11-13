from app import db
from datetime import datetime, timedelta


class Memo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String())
    content = db.Column(db.String())
    date = db.Column(db.DateTime, default=lambda:(datetime.utcnow()+timedelta(hours=7)).replace(microsecond=0))
    deadline = db.Column(db.String())
    
