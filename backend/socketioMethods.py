from db import db
from models.serverLogsModel import ServerLogs

from sqlalchemy import func, and_
import json
from datetime import datetime

class socketioClass():
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


    def query_database_for_new_records(last_checked_timestamps):
        # Convert last_checked_timestamps to a dictionary if it's not already
        if not isinstance(last_checked_timestamps, dict):
            return []

        # print("Last Checked Timestamps:", last_checked_timestamps)

        latest_logs_data = []

        # Subquery to get the maximum timestamp for each server
        subquery = db.session.query(ServerLogs.InfrastructureName, func.max(ServerLogs.LogDateTime).label("max_logDateTime")).group_by(ServerLogs.InfrastructureName).subquery()

        # Query to fetch the latest log entry for each server
        query = db.session.query(ServerLogs).join(subquery, and_(ServerLogs.InfrastructureName == subquery.c.InfrastructureName, ServerLogs.LogDateTime == subquery.c.max_logDateTime))

        if not last_checked_timestamps:
            latest_server_logs = query.all()

            print("Latest Server Logs:", latest_server_logs)

            # Convert the latest server logs to a list of dictionaries
            for record in latest_server_logs:
                log_data = record.__dict__
                # Convert LogDateTime to string format
                log_data['LogDateTime'] = str(log_data['LogDateTime'])
                # Remove unnecessary keys from the dictionary (e.g., '_sa_instance_state')
                log_data.pop('_sa_instance_state', None)
                latest_logs_data.append(log_data)

        else: 
            for server, last_checked_timestamp in last_checked_timestamps.items():
                # Convert last_checked_timestamp to a datetime object for comparison
                last_checked_datetime = last_checked_timestamp if last_checked_timestamp else None

                # Filter the query based on the last checked timestamp for the current server
                query_filtered = query.filter(ServerLogs.InfrastructureName == server)
                if last_checked_datetime:
                    query_filtered = query_filtered.filter(ServerLogs.LogDateTime > last_checked_datetime)

                latest_server_logs = query_filtered.all()

                # Convert the latest server logs to a list of dictionaries
                for record in latest_server_logs:
                    log_data = record.__dict__
                    # Convert LogDateTime to string format
                    log_data['LogDateTime'] = str(log_data['LogDateTime'])
                    # Remove unnecessary keys from the dictionary (e.g., '_sa_instance_state')
                    log_data.pop('_sa_instance_state', None)
                    latest_logs_data.append(log_data)

        return latest_logs_data


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

        print("Latest Timestamps:", latest_timestamps)
        return latest_timestamps


    def update_last_checked_timestamps(timestamps):
        # Convert datetime objects to string format
        serialized_timestamps = {server: timestamp.isoformat() for server, timestamp in timestamps.items()}

        # Update the last checked timestamps in the persistent storage or cache
        # For simplicity, let's assume it's stored in a file called 'last_checked_timestamps.json'
        with open('last_checked_timestamps.json', 'w') as file:
            file.write(json.dumps(serialized_timestamps))

