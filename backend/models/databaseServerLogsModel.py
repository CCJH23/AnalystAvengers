from db import db

class DatabaseServerLogs(db.Model):
    __tablename__ = 'DatabaseServerLogs'

    SN = db.Column(db.Integer, primary_key=True)
    ServerName = db.Column(db.String(255))
    Type = db.Column(db.String(255))
    Timestamp = db.Column(db.DateTime)
    Availability = db.Column(db.Integer)

