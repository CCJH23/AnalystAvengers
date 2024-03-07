from db import db

class MappingGraph(db.Model):
    __tablename__ = 'MappingGraph'

    Id = db.Column(db.Integer, primary_key=True)
    ParentEdge = db.Column(db.String(255), nullable=False)
    ChildEdge = db.Column(db.String(255), nullable=False)
    ServiceGroup = db.Column(db.Integer, nullable=False)
