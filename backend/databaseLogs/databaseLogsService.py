from models.databaseLogsModel import DatabaseLogs
from db import db
from flask import jsonify
from sqlalchemy import func, and_

class databaseLogsClass():
    # Retrieve all records from the DatabaseLogs table
    def get_database_logs():
        records = DatabaseLogs.query.all()
        
        # List to store database logs
        database_logs = []
        
        # Iterate through each record
        for record in records:
            # Convert record to a dictionary
            log_data = record.__dict__
            # Remove unnecessary keys from the dictionary (e.g., '_sa_instance_state')
            log_data.pop('_sa_instance_state', None)
            # Append database server log data to the list
            database_logs.append(log_data)
            
        if database_logs:
            # Return JSON response with database logs
            return jsonify({"code": 200, "data": {"database_server_logs": database_logs}}), 200
        else:
            # Return JSON response indicating no database logs are available
            return jsonify({"code": 404, "message": "There are no database logs available."}), 404

    # Get records of each database by unique InfrastructureName, from the DatabaseLogs table with the latest logdatetime
    def get_latest_database_logs():
        try:
            # Subquery to get the maximum logdatetime for each database
            subquery = db.session.query(DatabaseLogs.InfrastructureName, func.max(DatabaseLogs.LogDateTime).label("max_logdatetime")).group_by(DatabaseLogs.InfrastructureName).subquery()

            # Query to fetch the latest log entry for each database
            latest_database_logs = db.session.query(DatabaseLogs).join(subquery, and_(DatabaseLogs.InfrastructureName == subquery.c.InfrastructureName, DatabaseLogs.LogDateTime == subquery.c.max_logdatetime)).all()

            # List to store latest database logs
            latest_logs_data = []

            # Iterate through each record
            for record in latest_database_logs:
                # Convert record to a dictionary
                log_data = record.__dict__
                # Remove unnecessary keys from the dictionary (e.g., '_sa_instance_state')
                log_data.pop('_sa_instance_state', None)
                # Append latest database log data to the list
                latest_logs_data.append(log_data)

            if latest_logs_data:
                # Return JSON response with the latest database logs
                return jsonify({"code": 200, "data": {"latest_database_logs": latest_logs_data}}), 200
            else:
                # Return JSON response indicating no database logs are available
                return jsonify({"code": 404, "message": "There are no database logs available."}), 404
        except Exception as e:
            # Handle any exceptions and return an error response
            return jsonify({"code": 500, "message": f"An error occurred: {str(e)}"}), 500

