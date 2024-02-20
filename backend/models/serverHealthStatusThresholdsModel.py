from db import db

class ServerHealthStatusThresholds(db.Model):
    __tablename__ = 'ServerHealthStatusThresholds'

    Metric = db.Column(db.String(50), primary_key=True)
    CriticalThreshold = db.Column(db.Integer)
    BadThreshold = db.Column(db.Integer)
    WarningThreshold = db.Column(db.Integer)

