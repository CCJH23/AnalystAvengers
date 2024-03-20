from db import db

class MappingGraph(db.Model):
    __tablename__ = 'MappingGraph'

    Id = db.Column(db.Integer, primary_key=True)
    ParentEdge = db.Column(db.String(255))
    ChildEdge = db.Column(db.String(255))
    ServiceGroup = db.Column(db.Integer)