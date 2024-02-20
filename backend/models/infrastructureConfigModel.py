from db import db

class InfrastructureConfig(db.Model):
    __tablename__ = 'InfrastructureConfig'

    ServerName = db.Column(db.String(255), primary_key=True)
    Type = db.Column(db.String(255), primary_key=True)
    MonitoringTool = db.Column(db.String(255))
    Priority = db.Column(db.Integer)
    Country = db.Column(db.String(255))

