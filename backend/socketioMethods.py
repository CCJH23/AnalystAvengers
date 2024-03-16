from db import db
from models.serverLogsModel import ServerLogs
from models.databaseLogsModel import DatabaseLogs
from models.webAppLogsModel import WebAppLogs
from models.metricThresholdModel import MetricThreshold
from models.problemLogsModel import ProblemLogs
from metricThreshold.metricThresholdService import metricThresholdClass


from sqlalchemy import func, and_
import json
import pytz
from datetime import datetime, timedelta
from flask import jsonify


class socketioClass():
    def query_database_for_new_serverlogs_records():

        latest_logs_data = []

        # Subquery to get the maximum timestamp for each server
        subquery = db.session.query(ServerLogs.InfrastructureName, func.max(ServerLogs.LogDateTime).label("max_logDateTime")).group_by(ServerLogs.InfrastructureName).subquery()

        # Query to fetch the latest log entry for each server
        query = db.session.query(ServerLogs).join(subquery, and_(ServerLogs.InfrastructureName == subquery.c.InfrastructureName, ServerLogs.LogDateTime == subquery.c.max_logDateTime))

        latest_server_logs = query.all()

        # print("Latest Server Logs:", latest_server_logs)

        # Convert the latest server logs to a list of dictionaries
        for record in latest_server_logs:
            log_data = record.__dict__
            # Convert LogDateTime to string format
            log_data['LogDateTime'] = str(log_data['LogDateTime'])
            # Remove unnecessary keys from the dictionary (e.g., '_sa_instance_state')
            log_data.pop('_sa_instance_state', None)
            latest_logs_data.append(log_data)
        
        return latest_logs_data
    

    def query_database_for_metrics_records():
        latest_logs_data = []
        model_array = [ServerLogs, WebAppLogs]
        
        for model in model_array:
            # Subquery to get the maximum timestamp for each server
            subquery = db.session.query(model.InfrastructureName, func.max(model.LogDateTime).label("max_logDateTime")).group_by(model.InfrastructureName).subquery()

            # Query to fetch the latest log entry for each server
            query = db.session.query(model).join(subquery, and_(model.InfrastructureName == subquery.c.InfrastructureName, model.LogDateTime == subquery.c.max_logDateTime))

            latest_server_logs = query.all()

            # Convert the latest server logs to a list of dictionaries
            for record in latest_server_logs:
                log_data = record.__dict__
                # Convert LogDateTime to string format
                log_data['LogDateTime'] = str(log_data['LogDateTime'])
                # Remove unnecessary keys from the dictionary (e.g., '_sa_instance_state')
                log_data.pop('_sa_instance_state', None)
                latest_logs_data.append(log_data)

        # print("Latest Logs Data:", latest_logs_data)
        return latest_logs_data


    def get_historical_serverlogs_records(start_time, end_time):
        # Initialize a list to store historical logs
        historical_logs_data = []
        # Query to fetch historical logs within the specified time frame
        query = db.session.query(ServerLogs).filter(ServerLogs.LogDateTime >= start_time, ServerLogs.LogDateTime <= end_time)

        # Fetch historical logs
        historical_logs = query.all()

        # Convert historical logs to a list of dictionaries
        for record in historical_logs:
            log_data = record.__dict__
            # Convert LogDateTime to string format
            log_data['LogDateTime'] = str(log_data['LogDateTime'])
            # Remove unnecessary keys from the dictionary (e.g., '_sa_instance_state')
            log_data.pop('_sa_instance_state', None)
            historical_logs_data.append(log_data)

        # print("<--------------------Historical Logs Data-------------------------")
        # print("Historical Logs Data:", historical_logs_data)
        # print("---------------------Historical Logs Data------------------------>")

        return historical_logs_data
    

    def get_historical_logs_records(start_time, end_time, infra_type):
        # Initialize a list to store historical logs
        model = None
        historical_logs_data = []
        if infra_type == "server":
            model = ServerLogs
        elif infra_type == "database":
            model = DatabaseLogs
        elif infra_type == "webapp":
            model = WebAppLogs

        # Query to fetch historical logs within the specified time frame
        query = db.session.query(model).filter(model.LogDateTime >= start_time, model.LogDateTime <= end_time)

        # Fetch historical logs
        historical_logs = query.all()

        # Convert historical logs to a list of dictionaries
        for record in historical_logs:
            log_data = record.__dict__
            # Convert LogDateTime to string format
            log_data['LogDateTime'] = str(log_data['LogDateTime'])
            # Remove unnecessary keys from the dictionary (e.g., '_sa_instance_state')
            log_data.pop('_sa_instance_state', None)
            historical_logs_data.append(log_data)

        # print("<--------------------Historical Logs Data-------------------------")
        # print("Historical Logs Data:", historical_logs_data)
        # print("---------------------Historical Logs Data------------------------>")

        return historical_logs_data
    

    # def get_health_status_socket(latest_server_logs):
    #     try:
    #         if latest_server_logs:

    #             # Fetch health status thresholds from the database
    #             # thresholds = MetricThreshold.query.all()
    #             # threshold_dict = {threshold.Metric: (threshold.CriticalThreshold, threshold.BadThreshold, threshold.WarningThreshold) for threshold in thresholds}
    #             # print("Thresholds:", threshold_dict)
    #             threshold_dict = metricThresholdClass.get_metric_thresholds()

    #             # List to store health status data
    #             health_status_data = []

    #             # Iterate through each server log
    #             # print("Latest_server_logs are", latest_server_logs)
    #             for log in latest_server_logs:
    #                 infrastructure_name = log['InfrastructureName']
    #                 infrastructure_type = log['InfrastructureType']
    #                 logDateTime = log['LogDateTime']
    #                 overallHealthStatusSet = set()
    #                 overallHealthStatus = 'Healthy'
    #                 health_status = {}

    #                 # Determine health status for each metric
    #                 for metric in log.keys():
    #                     if metric in threshold_dict:
    #                         value = log[metric]
    #                         critical_threshold, bad_threshold, warning_threshold = threshold_dict[metric]

    #                         if metric == 'ServerAvailability' or metric == 'ServerNetworkAvailability':
    #                             if value == 0:
    #                                 health_status[metric] = 'Critical'
    #                                 overallHealthStatusSet.add('Critical')
    #                             else:
    #                                 health_status[metric] = 'Healthy'
    #                                 overallHealthStatusSet.add('Healthy')
    #                         else:
    #                             if value >= critical_threshold:
    #                                 health_status[metric] = 'Critical'
    #                                 overallHealthStatusSet.add('Critical')
    #                             elif value >= bad_threshold:
    #                                 health_status[metric] = 'Bad'
    #                                 overallHealthStatusSet.add('Bad')
    #                             elif value >= warning_threshold:
    #                                 health_status[metric] = 'Warning'
    #                                 overallHealthStatusSet.add('Warning')
    #                             else:
    #                                 health_status[metric] = 'Healthy'
    #                                 overallHealthStatusSet.add('Healthy')

    #                 if 'Critical' in overallHealthStatusSet:
    #                     overallHealthStatus = 'Critical'
    #                 elif 'Bad' in overallHealthStatusSet:
    #                     overallHealthStatus = 'Bad'
    #                 elif 'Warning' in overallHealthStatusSet:
    #                     overallHealthStatus = 'Warning'

    #                 # Append infrastructure name and its health status to the list
    #                 health_status_data.append({'InfrastructureName': infrastructure_name, 'InfrastructureType': infrastructure_type, 'LogDateTime': logDateTime, 'OverallHealthStatus': overallHealthStatus, 'HealthStatus': health_status})

    #             if health_status_data:
    #                 return jsonify({"code": 200, "data": health_status_data}), 200
    #             else:
    #                 return jsonify({"code": 404, "message": "No server logs available."}), 404
    #         else:
    #             # Return the response from get_latest_server_logs() directly
    #             return jsonify({"code": 404, "message": "No server logs available."}), 404
    #     except Exception as e:
    #         # Handle any exceptions and return an error response
    #         return jsonify({"code": 500, "message": f"An error occurred: {str(e)}"}), 500

        
    def get_problem_logs():

        problem_logs_data = []

        # try:
        problemLogs = ProblemLogs.query.all()
        for record in problemLogs:
            log_data = record.__dict__
            # Convert LogDateTime to string format
            log_data['LogDateTime'] = str(log_data['LogDateTime'])
            # Remove unnecessary keys from the dictionary (e.g., '_sa_instance_state')
            log_data.pop('_sa_instance_state', None)
            problem_logs_data.append(log_data)

        # print("Problem_logs_data:", problem_logs_data)
        
        return problem_logs_data 


    def get_latest_problem_logs():
        latest_problem_logs_data = []

        # Get the current time in GMT timezone
        gmt = pytz.timezone('GMT')
        current_time = datetime.now(gmt)

        # Calculate the start time as 15 seconds ago from the current time
        start_time = current_time - timedelta(seconds=15)

        # Query to fetch the problem logs within the past 15 seconds
        query = db.session.query(ProblemLogs).filter(ProblemLogs.LogDateTime >= start_time)

        latest_problem_logs = query.all()

        # Convert the latest problem logs to a list of dictionaries
        for record in latest_problem_logs:
            log_data = record.__dict__
            # Convert LogDateTime to string format
            log_data['LogDateTime'] = str(log_data['LogDateTime'])
            # Remove unnecessary keys from the dictionary (e.g., '_sa_instance_state')
            log_data.pop('_sa_instance_state', None)
            latest_problem_logs_data.append(log_data)

        # print("Latest Problem Logs:", latest_problem_logs_data)

        return latest_problem_logs_data

    
    # Get health status by problem severity
    def get_health_status_by_severity(severity):
        # severity == 0-1, healthy
        # severity == 2, degraded
        # severity == 3-5, unhealthy
        if severity == 0 or severity == 1:
            return "Healthy"
        elif severity == 2:
            return "Degraded"
        else:
            return "Unhealthy"
        

    def get_health_status_socket(latest_problem_logs_data, new_records):
        health_status = {}
        
        # Initialize overall severity as Healthy for all infrastructure names in new_records
        for record in new_records:
            infrastructure_name = record['InfrastructureName']
            health_status[infrastructure_name] = "Healthy"

        # Update the health status based on the latest problem logs
        for record in latest_problem_logs_data:
            infrastructure_name = record['InfrastructureName']
            problem_severity = record['ProblemSeverity']
            
            if infrastructure_name not in health_status:
                # If infrastructure name not found in new_records, initialize it with Healthy
                health_status[infrastructure_name] = "Healthy"

            # Update the severity if the problem severity is worse than the current one
            current_severity = health_status.get(infrastructure_name, "Healthy")
            if problem_severity == 2 and current_severity != "Unhealthy":
                health_status[infrastructure_name] = "Degraded"
            elif problem_severity >= 3:
                health_status[infrastructure_name] = "Unhealthy"

        return health_status

        






# ============================================UNUSED CODE================================================
        
    def get_latest_timestamp(records):
        # Initialize a dictionary to store the latest timestamp for each unique server
        latest_timestamps = {}

        # Iterate through the records to find the latest timestamp for each server
        for record in records:
            timestamp = datetime.strptime(record['LogDateTime'], '%Y-%m-%d %H:%M:%S')
            infrastructure_name = record['InfrastructureName']

            # Update the latest timestamp for the server if it's later than the current one
            if infrastructure_name not in latest_timestamps or timestamp > latest_timestamps[infrastructure_name]:
                latest_timestamps[infrastructure_name] = timestamp

        # print("Latest Timestamps:", latest_timestamps)
        return latest_timestamps


    def update_last_checked_timestamps(timestamps):
        # Convert datetime objects to string format
        serialized_timestamps = {server: timestamp.isoformat() for server, timestamp in timestamps.items()}

        # Update the last checked timestamps in the persistent storage or cache
        # For simplicity, let's assume it's stored in a file called 'last_checked_timestamps.json'
        with open('last_checked_timestamps.json', 'w') as file:
            file.write(json.dumps(serialized_timestamps))

    def get_last_checked_timestamps():
        # Retrieve the last checked timestamps from a persistent storage or cache
        # For simplicity, let's assume it's stored in a file called 'last_checked_timestamps.json'
        try:
            with open('last_checked_timestamps.json', 'r') as file:
                timestamps_str = file.read().strip()
                if timestamps_str:
                    return json.loads(timestamps_str)
                else:
                    return {}
        except FileNotFoundError:
            return {}