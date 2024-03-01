from models.MappingGraphModel import MappingGraphModel
from flask import jsonify

class MappingGraphClass():
    # Get all records from MappingGraphClass table
    def get_mapping_graph():
        # Retrieve all records from the MappingGraph table
        records = MappingGraphModel.query.all()

        # List to store mappings
        return records
    
