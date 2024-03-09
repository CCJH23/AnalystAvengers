from models.problemLogsModel import ProblemLogs
from flask import jsonify

class problemLogsClass():
    # Get all records from the ProblemLogs table
    def get_problem_logs():
        # Retrieve all records from the ProblemLogs table
        records = ProblemLogs.query.all()
        
        # List to store problem logs
        problem_logs = []
        
        # Iterate through each record
        for record in records:
            # Convert record to a dictionary
            log_data = record.__dict__
            # Remove unnecessary keys from the dictionary (e.g., '_sa_instance_state')
            log_data.pop('_sa_instance_state', None)
            # Append problem log data to the list
            problem_logs.append(log_data)
            
        if problem_logs:  # Check if problem logs are available
            # Return JSON response with problem logs
            return jsonify({"code": 200, "data": {"problem_logs": problem_logs}}), 200
        else:
            # Return JSON response indicating no problem logs are available
            return jsonify({"code": 404, "message": "There are no problem logs available."}), 404

