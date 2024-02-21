#########
# IMPORTS
#########
# internal imports
from db import db
from models.serverLogsModel import ServerLogs
from infrastructureConfig.infrastructureConfigController import infrastructureConfigBp
from serverLogs.serverLogsController import serverLogsBp
from webAppLogs.webAppLogsController import webAppLogsBp
from databaseLogs.databaseLogsController import databaseLogsBp
from metricThreshold.metricThresholdController import metricThresholdBp

# external imports
from dotenv import load_dotenv
import os
from flask import Flask
from flask_socketio import SocketIO, emit
from sqlalchemy import text, func, and_ #func is a module provided by SQLAlchemy that allows usage of SQL functions in queries. and_ is a logical operator provided by SQLAlchemy that constructs an SQL AND clause.
from flask_cors import CORS
import time, datetime, json
from threading import Thread
from datetime import datetime
#############################
# INITIALISATIONS OF APP, etc
#############################
app = Flask(__name__)
CORS(app)

# initialise web socket
socketio = SocketIO(app, cors_allowed_origins="*")

# initialise database with Flask app
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pyodbc://analystavengers:{os.environ["DATABASE_PASSWORD"]}@analystavengersdb.database.windows.net:1433/AnalystAvenger_SQL?driver=ODBC+Driver+18+for+SQL+Server'
db.init_app(app)

# register blueprints
app.register_blueprint(infrastructureConfigBp)
app.register_blueprint(serverLogsBp)
app.register_blueprint(webAppLogsBp)
app.register_blueprint(databaseLogsBp)
app.register_blueprint(metricThresholdBp)

################
# DEFAULT ROUTES
################
@app.route('/')
def hello_world():
    if check_db_connection():
        return "Connection to the database established!"
    else:
        return "Failed to connect to the database."

# Check the database connection
def check_db_connection():
    try:
        # Obtain a connection from the engine
        conn = db.engine.connect()
        
        # Execute a simple query against one of the tables
        query = text("SELECT TOP 1 * FROM dbo.InfrastructureConfig ORDER BY ServerName")
        result = conn.execute(query)
        
        # Close the connection
        conn.close()
        
        return True
    except Exception as e:
        print(f"Error connecting to the database: {str(e)}")
        return False


#---SocketIO---#
# @socketio.on('serverlog', namespace='/latestlogs')
# def handle_server_logs_connect():
#     try:
#         # Subquery to get the maximum timestamp for each server
#         subquery = db.session.query(ServerLogs.InfrastructureName, func.max(ServerLogs.LogDateTime).label("max_timestamp")).group_by(ServerLogs.InfrastructureName).subquery()

#         # Query to fetch the latest log entry for each server
#         latest_server_logs = db.session.query(ServerLogs).join(subquery, and_(ServerLogs.InfrastructureName == subquery.c.InfrastructureName, ServerLogs.LogDateTime == subquery.c.max_timestamp)).all()

#         print("Latest Server Logs:", latest_server_logs)

#         # List to store latest server logs
#         latest_logs_data = []

#         # Iterate through each record
#         for record in latest_server_logs:
#             record.LogDateTime = str(record.LogDateTime)
#             # Convert record to a dictionary
#             log_data = record.__dict__
#             # Remove unnecessary keys from the dictionary (e.g., '_sa_instance_state')
#             log_data.pop('_sa_instance_state', None)
#             # Append latest server log data to the list
#             latest_logs_data.append(log_data)

#         print("Latest Server Logs Data:", latest_logs_data)

#         if latest_logs_data:
#             # Emit WebSocket event with the latest server logs
#             emit('latest_server_logs', {"code": 200, "data": {"latest_server_logs": latest_logs_data}})
#         else:
#             # Emit WebSocket event indicating no server logs are available
#             emit('latest_server_logs', {"code": 404, "message": "There are no server logs available."})
#     except Exception as e:
#         # Emit WebSocket event for error response
#         emit('latest_server_logs', {"code": 500, "message": f"An error occurred: {str(e)}"})


# if __name__ == "__main__":
#     socketio.run(app, port=8000, debug=True)
    # app.run(port=8000, debug=True)

# Function to continuously poll the database for changes
def poll_database_for_changes():
    with app.app_context():
        last_checked_timestamp = get_last_checked_timestamps()
        print("Last Checked Timestamps:", last_checked_timestamp)
        while True:
            new_records = query_database_for_new_records(last_checked_timestamp)
            print("New Records:", new_records)

            if new_records:
                socketio.emit('latest_server_logs', {"code": 200, "data": {"latest_server_logs": new_records}}, namespace='/latestlogs')

            last_checked_timestamp = get_latest_timestamp(new_records)
            # print("Last Checked Timestamps:", last_checked_timestamp)
            update_last_checked_timestamps(last_checked_timestamp)
            
            time.sleep(10)  # Adjust the interval as needed

# Function to query the database for new records
# def query_database_for_new_records(last_checked_timestamp):
#     # Convert last_checked_timestamp to a datetime object for comparison
#     print(last_checked_timestamp)
#     print(type(last_checked_timestamp))
#     # last_checked_datetime = datetime.fromtimestamp(last_checked_timestamp) if last_checked_timestamp else None
#     last_checked_datetime = last_checked_timestamp if last_checked_timestamp else None
    
#     # Subquery to get the maximum timestamp for each server
#     subquery = db.session.query(ServerLogs.InfrastructureName, func.max(ServerLogs.LogDateTime).label("max_timestamp")).group_by(ServerLogs.InfrastructureName).subquery()

#     # Query to fetch the latest log entry for each server
#     query = db.session.query(ServerLogs).join(subquery, and_(ServerLogs.InfrastructureName == subquery.c.InfrastructureName, ServerLogs.LogDateTime == subquery.c.max_timestamp))

#     # Filter the query based on the last checked timestamp
#     if last_checked_datetime:
#         query = query.filter(ServerLogs.LogDateTime > last_checked_datetime)

#     latest_server_logs = query.all()

#     # Convert the latest server logs to a list of dictionaries
#     latest_logs_data = []
#     for record in latest_server_logs:
#         log_data = record.__dict__
#         # Convert LogDateTime to string format
#         log_data['LogDateTime'] = str(log_data['LogDateTime'])
#         # Remove unnecessary keys from the dictionary (e.g., '_sa_instance_state')
#         log_data.pop('_sa_instance_state', None)
#         latest_logs_data.append(log_data)

#     return latest_logs_data

def query_database_for_new_records(last_checked_timestamps):
    # Convert last_checked_timestamps to a dictionary if it's not already
    if not isinstance(last_checked_timestamps, dict):
        return []

    # print("Last Checked Timestamps:", last_checked_timestamps)

    latest_logs_data = []

    # Subquery to get the maximum timestamp for each server
    subquery = db.session.query(ServerLogs.InfrastructureName, func.max(ServerLogs.LogDateTime).label("max_timestamp")).group_by(ServerLogs.InfrastructureName).subquery()

    # Query to fetch the latest log entry for each server
    query = db.session.query(ServerLogs).join(subquery, and_(ServerLogs.InfrastructureName == subquery.c.InfrastructureName, ServerLogs.LogDateTime == subquery.c.max_timestamp))

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



# def get_last_checked_timestamp():
#     # Retrieve the last checked timestamp from a persistent storage or cache
#     # For simplicity, let's assume it's stored in a file called 'last_checked_timestamp.txt'
#     try:
#         with open('last_checked_timestamp.txt', 'r') as file:
#             timestamp_str = file.read().strip()
#             if timestamp_str:
#                 return datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
#             else:
#                 return None
#     except FileNotFoundError:
#         return None

# def update_last_checked_timestamp(timestamp):
#     # Update the last checked timestamp in the persistent storage or cache
#     # For simplicity, let's assume it's stored in a file called 'last_checked_timestamp.txt'
#     with open('last_checked_timestamp.txt', 'w') as file:
#         file.write(str(timestamp))


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

import json

def update_last_checked_timestamps(timestamps):
    # Convert datetime objects to string format
    serialized_timestamps = {server: timestamp.isoformat() for server, timestamp in timestamps.items()}

    # Update the last checked timestamps in the persistent storage or cache
    # For simplicity, let's assume it's stored in a file called 'last_checked_timestamps.json'
    with open('last_checked_timestamps.json', 'w') as file:
        file.write(json.dumps(serialized_timestamps))



    
# def get_latest_timestamp(records):
#     # Get the timestamp of the latest record
#     if records:
#         # Extract timestamps from the records
#         timestamps = [datetime.strptime(record['LogDateTime'], '%Y-%m-%d %H:%M:%S') for record in records]
#         # Find the maximum timestamp
#         return max(timestamps)
#     else:
#         return None
        

# def get_latest_timestamp(records):
#     # Get the timestamp of the latest record for each unique server
#     last_checked_timestamps = {}
#     for record in records:
#         timestamp = datetime.strptime(record['LogDateTime'], '%Y-%m-%d %H:%M:%S')
#         infrastructure_name = record['InfrastructureName']
#         if infrastructure_name not in last_checked_timestamps or timestamp > last_checked_timestamps[infrastructure_name]:
#             last_checked_timestamps[infrastructure_name] = timestamp

#     return last_checked_timestamps

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



@socketio.on('serverlog', namespace='/latestlogs')
def handle_server_logs_connect():
    pass  # No action required on client connection

if __name__ == "__main__":
    # Start the polling process in a separate thread
    polling_thread = Thread(target=poll_database_for_changes)
    polling_thread.daemon = True
    polling_thread.start()

    # Start the Flask-SocketIO server
    socketio.run(app, port=8000, debug=True)