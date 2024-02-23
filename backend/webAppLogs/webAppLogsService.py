from models.webAppLogsModel import WebAppLogs
from db import db
from flask import jsonify
from sqlalchemy import func, and_

class webAppLogsClass():
    # Retrieve all records from the WebAppLogs table
    def get_web_app_logs():
        records = WebAppLogs.query.all()
        
        # List to store web app logs
        web_app_logs = []
        
        # Iterate through each record
        for record in records:
            # Convert record to a dictionary
            log_data = record.__dict__
            # Remove unnecessary keys from the dictionary (e.g., '_sa_instance_state')
            log_data.pop('_sa_instance_state', None)
            # Append web app log data to the list
            web_app_logs.append(log_data)
            
        if web_app_logs:  # Check if web app logs are available
            # Return JSON response with web app logs
            return jsonify({"code": 200, "data": {"web_app_logs": web_app_logs}}), 200
        else:
            # Return JSON response indicating no web app logs are available
            return jsonify({"code": 404, "message": "There are no web app logs available."}), 404

    # Get records of each entry by unique InfrastructureName, from the WebAppLogs table with the latest LogDateTime
    def get_latest_web_app_logs():
        try:
            # Subquery to get the maximum LogDateTime for each webapp
            subquery = db.session.query(WebAppLogs.InfrastructureName, func.max(WebAppLogs.LogDateTime).label("max_logdatetime")).group_by(WebAppLogs.InfrastructureName).subquery()

            # Query to fetch the latest log entry for each webapp
            latest_web_app_logs = db.session.query(WebAppLogs).join(subquery, and_(WebAppLogs.InfrastructureName == subquery.c.InfrastructureName, WebAppLogs.LogDateTime == subquery.c.max_logdatetime)).all()

            # List to store latest web app logs
            latest_logs_data = []

            # Iterate through each record
            for record in latest_web_app_logs:
                # Convert record to a dictionary
                log_data = record.__dict__
                # Remove unnecessary keys from the dictionary (e.g., '_sa_instance_state')
                log_data.pop('_sa_instance_state', None)
                # Append latest web app log data to the list
                latest_logs_data.append(log_data)

            if latest_logs_data:
                # Return JSON response with the latest web app logs
                return jsonify({"code": 200, "data": {"latest_web_app_logs": latest_logs_data}}), 200
            else:
                # Return JSON response indicating no web app logs are available
                return jsonify({"code": 404, "message": "There are no web app logs available."}), 404
        except Exception as e:
            # Handle any exceptions and return an error response
            return jsonify({"code": 500, "message": f"An error occurred: {str(e)}"}), 500

