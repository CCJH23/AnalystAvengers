from flask import jsonify, Blueprint
from problemLogs.problemLogsService import problemLogsClass

# initialise blueprint
problemLogsBp = Blueprint('problemLogs', __name__, url_prefix='/problemlogs')

# initialise route and service to call
# Get all records from the ProblemLogs table
@problemLogsBp.route('/problem_logs', methods=['GET'])
def get_problem_logs():
    try:
        response = problemLogsClass.get_problem_logs()
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

