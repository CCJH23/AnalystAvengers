from db import db

class ServerLogs(db.Model):
    # test table name is ServerLogsTest while table with actual data is ServerLogs
    __tablename__ = 'ServerLogsTest'

    Id = db.Column(db.Integer, primary_key=True)
    InfrastructureName = db.Column(db.String(255))
    InfrastructureType = db.Column(db.String(255))
    LogDateTime = db.Column(db.DateTime)
    ServerAvailability = db.Column(db.Integer)
    ServerDiskUtilisation = db.Column(db.Float)
    ServerMemoryUtilisation = db.Column(db.Float)
    ServerCpuUtilisation = db.Column(db.Float)
    ServerNetworkAvailability = db.Column(db.Integer)

