from db import db

class WebAppLogs(db.Model):
    # test table name is WebAppLogsTest while table with actual data is WebAppLogs
    __tablename__ = 'WebAppLogs'

    Id = db.Column(db.Integer, primary_key=True)
    InfrastructureName = db.Column(db.String(255))
    InfrastructureType = db.Column(db.String(255))
    LogDateTime = db.Column(db.DateTime)
    WebAppAvailability = db.Column(db.Integer)
    WebAppRate = db.Column(db.Integer)
    WebAppError = db.Column(db.Integer)
    WebAppDuration = db.Column(db.Integer)

