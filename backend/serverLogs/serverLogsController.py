from flask import jsonify, Blueprint
from serverLogs.serverLogsService import serverLogsClass

# initialise blueprint
serverLogsBp = Blueprint('serverLogs', __name__, url_prefix='/serverlogs')

# initialise route and service to call
# Get all records from the ServerLogs table
@serverLogsBp.route('/server_logs', methods=['GET'])
def get_server_logs():
    try:
        response = serverLogsClass.get_server_logs()
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Get records of each entry by unique ServerName, from the ServerLogs table with the latest Timestamp
@serverLogsBp.route('/server_logs/latest', methods=['GET'])
def get_latest_server_logs():
    try:
        response = serverLogsClass.get_latest_server_logs()
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

