from models.MappingGraphModel import MappingGraphModel
from flask import jsonify

class MappingGraphClass():
    # Get all records from MappingGraphClass table
    def get_mapping_graph():
        # Retrieve all records from the MappingGraph table
        records = MappingGraphModel.query.all()

        # Store retrieved records in array format
        mapped_records = [{"ParentEdge": record.ParentEdge, "ChildEdge": record.ChildEdge} for record in records]
        # List to store mappings
        return mapped_records