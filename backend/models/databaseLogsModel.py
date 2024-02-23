from db import db

class DatabaseLogs(db.Model):
    # test table name is DatabaseLogsTest while table with actual data is DatabaseLogs
    __tablename__ = 'DatabaseLogsTest'

    Id = db.Column(db.Integer, primary_key=True)
    InfrastructureName = db.Column(db.String(255))
    InfrastructureType = db.Column(db.String(255))
    LogDateTime = db.Column(db.DateTime)
    DatabaseAvailability = db.Column(db.Integer)

