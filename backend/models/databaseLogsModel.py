from db import db

class DatabaseLogs(db.Model):
    __tablename__ = 'DatabaseLogs'

    Id = db.Column(db.Integer, primary_key=True)
    InfrastructureName = db.Column(db.String(255))
    InfrastructureType = db.Column(db.String(255))
    LogDateTime = db.Column(db.DateTime)
    DatabaseAvailability = db.Column(db.Integer)
    DatabaseUptime = db.Column(db.Integer)
    DatabaseAvailableConnections = db.Column(db.Float)
    DatabaseSlowQueryRate = db.Column(db.Float)

