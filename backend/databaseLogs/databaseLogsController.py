from flask import jsonify, Blueprint
from databaseLogs.databaseLogsService import databaseLogsClass

# initialise blueprint
databaseLogsBp = Blueprint('databaseLogs', __name__, url_prefix='/databaselogs')

# initialise route and service to call
# Get all records from the DatabaseLogs table
@databaseLogsBp.route('/database_logs', methods=['GET'])
def get_database_logs():
    try:
        response = databaseLogsClass.get_database_logs()
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get records of each database by unique InfrastructureName, from the DatabaseLogs table with the latest logdatetime
@databaseLogsBp.route('/database_logs/latest', methods=['GET'])
def get_latest_database_logs():
    try:
        response = databaseLogsClass.get_latest_database_logs()
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

