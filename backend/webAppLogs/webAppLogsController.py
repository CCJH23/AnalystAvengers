from flask import jsonify, Blueprint
from webAppLogs.webAppLogsService import webAppLogsClass

# initialise blueprint
webAppLogsBp = Blueprint('webAppLogs', __name__, url_prefix='/webapplogs')

# initialise route and service to call
# Get all records from the WebAppLogs table
@webAppLogsBp.route('/web_app_logs', methods=['GET'])
def get_web_app_logs():
    try:
        response = webAppLogsClass.get_web_app_logs()
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Get records of each entry by unique InfrastructureName, from the WebAppLogs table with the latest LogDateTime
@webAppLogsBp.route('/web_app_logs/latest', methods=['GET'])
def get_latest_web_app_logs():
    try:
        response = webAppLogsClass.get_latest_web_app_logs()
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

