from db import db

class ServerLogs(db.Model):
    __tablename__ = 'ServerLogs'

    SN = db.Column(db.Integer, primary_key=True)
    ServerName = db.Column(db.String(255))
    Type = db.Column(db.String(255))
    Timestamp = db.Column(db.DateTime)
    Availability = db.Column(db.Integer)
    DiskUtilization = db.Column(db.Integer)
    MemoryUtilization = db.Column(db.Integer)
    CPUUtilization = db.Column(db.Integer)
    NetworkAvailability = db.Column(db.Integer)

