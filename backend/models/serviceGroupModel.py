from db import db

class ServiceGroup(db.Model):
    __tablename__ = 'ServiceGroup'

    ServiceId = db.Column(db.Integer, primary_key=True)
    ServiceName = db.Column(db.String(255), nullable=False)