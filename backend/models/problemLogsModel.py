from db import db

class ProblemLogs(db.Model):
    __tablename__ = 'ProblemLogs'

    Id = db.Column(db.Integer, primary_key=True)
    InfrastructureName = db.Column(db.String(255))
    LogDateTime = db.Column(db.DateTime)
    ProblemName = db.Column(db.String(255))
    ProblemSeverity = db.Column(db.String(255))

