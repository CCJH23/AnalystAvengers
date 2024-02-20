from flask import jsonify, Blueprint
from infrastructureConfig.infrastructureConfigService import infrastructureConfigClass

# initialise blueprint
infrastructureConfigBp = Blueprint('infrastructureConfig', __name__, url_prefix='/infrastructureconfig')

# initialise route and service to call
# Get all records from the InfrastructureConfig table
@infrastructureConfigBp.route('/infrastructure_config', methods=['GET'])
def get_infrastructure_config():
    try:
        response = infrastructureConfigClass.get_infrastructure_config()
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Query data from infrastructure_config table by infrastructure name and infrastructure type
@infrastructureConfigBp.route('/infrastructure_config/<infrastructure_name>/<infrastructure_type>', 
                            methods=['GET'])
def get_infrastructure_config_by_infra_name_and_type(infrastructure_name, infrastructure_type):
    try:
        response = infrastructureConfigClass.get_infrastructure_config_by_infra_name_and_type(infrastructure_name, infrastructure_type)
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500