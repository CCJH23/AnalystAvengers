from flask import jsonify, Blueprint
from serviceGroup.ServiceGroupService import ServiceGroupClass

# initialise blueprint
serviceGroupBp = Blueprint('serviceGroup', __name__, url_prefix='/serviceGroup')

# initialise route and service to call
# Get all records from the InfrastructureConfig table
@serviceGroupBp.route('/', methods=['GET'])
def get_infrastructure_config():
    try:
        response = ServiceGroupClass.get_service_group()
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500
