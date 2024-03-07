from flask import jsonify, Blueprint
from mappingGraph.MappingGraphService import MappingGraphClass

# initialise blueprint
mappingGraphBp = Blueprint('mappingGraph', __name__, url_prefix='/mappingGraph')

# initialise route and service to call
# Get all records from the InfrastructureConfig table
@mappingGraphBp.route('/', methods=['GET'])
def get_infrastructure_config():
    try:
        response = MappingGraphClass.get_mapping_graph()
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500
