from db import db

class MetricThreshold(db.Model):
    __tablename__ = 'MetricThreshold'

    Metric = db.Column(db.String(50), primary_key=True)
    CriticalThreshold = db.Column(db.Float)
    BadThreshold = db.Column(db.Float)
    WarningThreshold = db.Column(db.Float)

