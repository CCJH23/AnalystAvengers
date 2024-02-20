from db import db

class InfrastructureConfig(db.Model):
    # test table name is InfrastructureConfigTest while table with actual data is InfrastructureConfig
    __tablename__ = 'InfrastructureConfigTest'

    InfrastructureName = db.Column(db.String(255), primary_key=True)
    InfrastructureType = db.Column(db.String(255), primary_key=True)
    MonitoringTool = db.Column(db.String(255))
    InfrastructurePriority = db.Column(db.Integer)
    InfrastructureCountry = db.Column(db.String(255))

