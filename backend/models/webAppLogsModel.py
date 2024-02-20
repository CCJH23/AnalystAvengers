from db import db

class WebAppLogs(db.Model):
    __tablename__ = 'WebAppLogs'

    SN = db.Column(db.Integer, primary_key=True)
    ServerName = db.Column(db.String(255))
    Type = db.Column(db.String(255))
    Timestamp = db.Column(db.DateTime)
    Availability = db.Column(db.Integer)
    Rate = db.Column(db.Integer)
    Error = db.Column(db.Integer)
    Duration = db.Column(db.Integer)

