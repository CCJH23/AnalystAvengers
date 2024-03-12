from flask import jsonify, Blueprint
from metricThreshold.metricThresholdService import metricThresholdClass

# initialise blueprint
metricThresholdBp = Blueprint('metricThreshold', __name__, url_prefix='/metricthreshold')

# initialise route and service to call
# Get metric thresholds records from metricThreshold table
@metricThresholdBp.route('/metricthresholds', methods=['GET'])
def get_metric_thresholds():
    try:
        response = metricThresholdClass.get_metric_thresholds()
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Check the health status of the servers for server_logs table
@metricThresholdBp.route('/health_status', methods=['GET'])
def get_health_status():
    try:
        response = metricThresholdClass.get_health_status()
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

