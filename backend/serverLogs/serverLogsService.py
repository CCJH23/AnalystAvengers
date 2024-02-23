from models.serverLogsModel import ServerLogs
from db import db
from flask import jsonify
from sqlalchemy import func, and_

class serverLogsClass():
    # Get all records from the ServerLogs table
    def get_server_logs():
        # Retrieve all records from the ServerLogs table
        records = ServerLogs.query.all()
        
        # List to store server logs
        server_logs = []
        
        # Iterate through each record
        for record in records:
            # Convert record to a dictionary
            log_data = record.__dict__
            # Remove unnecessary keys from the dictionary (e.g., '_sa_instance_state')
            log_data.pop('_sa_instance_state', None)
            # Append server log data to the list
            server_logs.append(log_data)
            
        if server_logs:  # Check if server logs are available
            # Return JSON response with server logs
            return jsonify({"code": 200, "data": {"server_logs": server_logs}}), 200
        else:
            # Return JSON response indicating no server logs are available
            return jsonify({"code": 404, "message": "There are no server logs available."}), 404

    # Get records of each entry by unique ServerName, from the ServerLogs table with the latest Timestamp
    def get_latest_server_logs():
        try:
            # Subquery to get the maximum timestamp for each server
            subquery = db.session.query(ServerLogs.InfrastructureName, func.max(ServerLogs.LogDateTime).label("max_datetime")).group_by(ServerLogs.InfrastructureName).subquery()

            # Query to fetch the latest log entry for each server
            latest_server_logs = db.session.query(ServerLogs).join(subquery, and_(ServerLogs.InfrastructureName == subquery.c.InfrastructureName, ServerLogs.LogDateTime == subquery.c.max_datetime)).all()

            print(latest_server_logs)

            # List to store latest server logs
            latest_logs_data = []

            # Iterate through each record
            for record in latest_server_logs:
                # Convert record to a dictionary
                log_data = record.__dict__
                # Remove unnecessary keys from the dictionary (e.g., '_sa_instance_state')
                log_data.pop('_sa_instance_state', None)
                # Append latest server log data to the list
                latest_logs_data.append(log_data)

            if latest_logs_data:
                # Return JSON response with the latest server logs
                return jsonify({"code": 200, "data": {"latest_server_logs": latest_logs_data}}), 200
            else:
                # Return JSON response indicating no server logs are available
                return jsonify({"code": 404, "message": "There are no server logs available."}), 404
        except Exception as e:
            # Handle any exceptions and return an error response
            return jsonify({"code": 500, "message": f"An error occurred: {str(e)}"}), 500

