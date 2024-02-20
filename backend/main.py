# internal imports
from db import db
from models.infrastructureConfigModel import InfrastructureConfig
from models.serverLogsModel import ServerLogs
from models.webAppLogsModel import WebAppLogs
from models.databaseServerLogsModel import DatabaseServerLogs
from models.serverHealthStatusThresholdsModel import ServerHealthStatusThresholds

# external imports
from dotenv import load_dotenv
import os
import json
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from sqlalchemy import text, desc, func, and_ #func is a module provided by SQLAlchemy that allows usage of SQL functions in queries. and_ is a logical operator provided by SQLAlchemy that constructs an SQL AND clause.
from flask_cors import CORS
import pyodbc

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# initialise database with Flask app
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pyodbc://analystavengers:{os.environ["DATABASE_PASSWORD"]}@analystavengersdb.database.windows.net:1433/AnalystAvenger_SQL?driver=ODBC+Driver+18+for+SQL+Server'
db.init_app(app)

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


@app.route('/')
def hello_world():

    if check_db_connection():
        return "Connection to the database established!"
    else:
        return "Failed to connect to the database."
    
# Get all records from the InfrastructureConfig table
@app.route('/infrastructure_config', methods=['GET'])
def get_infrastructure_config():
    # Retrieve all records from the InfrastructureConfig table
    records = InfrastructureConfig.query.all()
    
    # List to store server configurations
    server_configurations = []
    
    # Iterate through each record
    for record in records:
        # Convert record to a dictionary
        config_data = record.__dict__
        # Remove unnecessary keys from the dictionary (e.g., '_sa_instance_state')
        config_data.pop('_sa_instance_state', None)
        # Append server configuration data to the list
        server_configurations.append(config_data)
        
    if server_configurations:  # Check if server configurations are available
        # Return JSON response with server configurations
        return jsonify({"code": 200, "data": {"server_configurations": server_configurations}}), 200
    else:
        # Return JSON response indicating no server configurations are available
        return jsonify({"code": 404, "message": "There are no server configurations available."}), 404
    
# Get all records from the ServerLogs table
@app.route('/server_logs', methods=['GET'])
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
    
# Get all records from the WebAppLogs table   
@app.route('/web_app_logs', methods=['GET'])
def get_web_app_logs():
    # Retrieve all records from the WebAppLogs table
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
    
# Get all records from the DatabaseServerLogs table   
@app.route('/database_server_logs', methods=['GET'])
def get_database_server_logs():
    # Retrieve all records from the DatabaseServerLogs table
    records = DatabaseServerLogs.query.all()
    
    # List to store database server logs
    database_server_logs = []
    
    # Iterate through each record
    for record in records:
        # Convert record to a dictionary
        log_data = record.__dict__
        # Remove unnecessary keys from the dictionary (e.g., '_sa_instance_state')
        log_data.pop('_sa_instance_state', None)
        # Append database server log data to the list
        database_server_logs.append(log_data)
        
    if database_server_logs:
        # Return JSON response with database server logs
        return jsonify({"code": 200, "data": {"database_server_logs": database_server_logs}}), 200
    else:
        # Return JSON response indicating no database server logs are available
        return jsonify({"code": 404, "message": "There are no database server logs available."}), 404

# Get records of each entry by unique ServerName, from the ServerLogs table with the latest Timestamp
@app.route('/server_logs/latest', methods=['GET'])
def get_latest_server_logs():
    try:
        # Subquery to get the maximum timestamp for each server
        subquery = db.session.query(ServerLogs.ServerName, func.max(ServerLogs.Timestamp).label("max_timestamp")).group_by(ServerLogs.ServerName).subquery()

        # Query to fetch the latest log entry for each server
        latest_server_logs = db.session.query(ServerLogs).join(subquery, and_(ServerLogs.ServerName == subquery.c.ServerName, ServerLogs.Timestamp == subquery.c.max_timestamp)).all()

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

# Get records of each entry by unique ServerName, from the DatabaseServerLogs table with the latest Timestamp
@app.route('/database_server_logs/latest', methods=['GET'])
def get_latest_database_server_logs():
    try:
        # Subquery to get the maximum timestamp for each server
        subquery = db.session.query(DatabaseServerLogs.ServerName, func.max(DatabaseServerLogs.Timestamp).label("max_timestamp")).group_by(DatabaseServerLogs.ServerName).subquery()

        # Query to fetch the latest log entry for each server
        latest_database_server_logs = db.session.query(DatabaseServerLogs).join(subquery, and_(DatabaseServerLogs.ServerName == subquery.c.ServerName, DatabaseServerLogs.Timestamp == subquery.c.max_timestamp)).all()

        # List to store latest database server logs
        latest_logs_data = []

        # Iterate through each record
        for record in latest_database_server_logs:
            # Convert record to a dictionary
            log_data = record.__dict__
            # Remove unnecessary keys from the dictionary (e.g., '_sa_instance_state')
            log_data.pop('_sa_instance_state', None)
            # Append latest database server log data to the list
            latest_logs_data.append(log_data)

        if latest_logs_data:
            # Return JSON response with the latest database server logs
            return jsonify({"code": 200, "data": {"latest_database_server_logs": latest_logs_data}}), 200
        else:
            # Return JSON response indicating no database server logs are available
            return jsonify({"code": 404, "message": "There are no database server logs available."}), 404
    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"code": 500, "message": f"An error occurred: {str(e)}"}), 500
    
# Get records of each entry by unique ServerName, from the WebAppLogs table with the latest Timestamp
@app.route('/web_app_logs/latest', methods=['GET'])
def get_latest_web_app_logs():
    try:
        # Subquery to get the maximum timestamp for each server
        subquery = db.session.query(WebAppLogs.ServerName, func.max(WebAppLogs.Timestamp).label("max_timestamp")).group_by(WebAppLogs.ServerName).subquery()

        # Query to fetch the latest log entry for each server
        latest_web_app_logs = db.session.query(WebAppLogs).join(subquery, and_(WebAppLogs.ServerName == subquery.c.ServerName, WebAppLogs.Timestamp == subquery.c.max_timestamp)).all()

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
  
# Query data from infrastructure_config table by server name and type
@app.route('/infrastructure_config/<server_name>/<type>', methods=['GET'])
def get_infrastructure_config_by_server_name_and_type(server_name, type):
    try:
        # Query to fetch the server configuration by server name and type
        config = InfrastructureConfig.query.filter_by(ServerName=server_name, Type=type).first()

        if config:
            # Convert record to a dictionary
            config_data = config.__dict__
            # Remove unnecessary keys from the dictionary (e.g., '_sa_instance_state')
            config_data.pop('_sa_instance_state', None)
            # Return JSON response with the server configuration
            return jsonify({"code": 200, "data": {"server_configuration": config_data}}), 200
        else:
            # Return JSON response indicating no server configuration is available
            return jsonify({"code": 404, "message": "There is no server configuration available for the specified server name and type."}), 404
    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"code": 500, "message": f"An error occurred: {str(e)}"}), 500


# Check the health status of the servers for server_logs table
@app.route('/health_status', methods=['GET'])
def get_health_status():
    try:
        # Fetch the latest server logs
        latest_server_logs_response = get_latest_server_logs()
        response, status_code = get_latest_server_logs()

        # Check if the response is successful
        if status_code == 200:
            # Extract the data from the response
            json_data = response.json

            latest_server_logs = json_data['data']['latest_server_logs']

            # Fetch health status thresholds from the database
            thresholds = ServerHealthStatusThresholds.query.all()
            threshold_dict = {threshold.Metric: (threshold.CriticalThreshold, threshold.BadThreshold, threshold.WarningThreshold) for threshold in thresholds}

            # List to store health status data
            health_status_data = []

            # Iterate through each server log
            for log in latest_server_logs:
                server_name = log['ServerName']
                health_status = {}

                # Determine health status for each metric
                for metric in log.keys():
                    if metric in threshold_dict:
                        value = log[metric]
                        critical_threshold, bad_threshold, warning_threshold = threshold_dict[metric]

                        if metric == 'Availability' or metric == 'NetworkAvailability':
                            if value == 0:
                                health_status[metric] = 'Critical'
                            else:
                                health_status[metric] = 'Healthy'
                        else:
                            if value >= critical_threshold:
                                health_status[metric] = 'Critical'
                            elif value >= bad_threshold:
                                health_status[metric] = 'Bad'
                            elif value >= warning_threshold:
                                health_status[metric] = 'Warning'
                            else:
                                health_status[metric] = 'Healthy'

                # Append server name and its health status to the list
                health_status_data.append({'ServerName': server_name, 'HealthStatus': health_status})

            if health_status_data:
                return jsonify({"code": 200, "data": health_status_data}), 200
            else:
                return jsonify({"code": 404, "message": "No server logs available."}), 404
        else:
            # Return the response from get_latest_server_logs() directly
            return latest_server_logs_response[0]
    except Exception as e:
        # Handle any exceptions and return an error response
        return jsonify({"code": 500, "message": f"An error occurred: {str(e)}"}), 500


#---SocketIO---#

@socketio.on('serverlog', namespace='/latestlogs')
def handle_server_logs_connect():
    try:
        # Subquery to get the maximum timestamp for each server
        subquery = db.session.query(ServerLogs.ServerName, func.max(ServerLogs.Timestamp).label("max_timestamp")).group_by(ServerLogs.ServerName).subquery()

        # Query to fetch the latest log entry for each server
        latest_server_logs = db.session.query(ServerLogs).join(subquery, and_(ServerLogs.ServerName == subquery.c.ServerName, ServerLogs.Timestamp == subquery.c.max_timestamp)).all()

        print("Latest Server Logs:", latest_server_logs)

        # List to store latest server logs
        latest_logs_data = []

        # Iterate through each record
        for record in latest_server_logs:
            record.Timestamp = str(record.Timestamp)
            # Convert record to a dictionary
            log_data = record.__dict__
            # Remove unnecessary keys from the dictionary (e.g., '_sa_instance_state')
            log_data.pop('_sa_instance_state', None)
            # Append latest server log data to the list
            latest_logs_data.append(log_data)

        print("Latest Server Logs Data:", latest_logs_data)

        if latest_logs_data:
            # Emit WebSocket event with the latest server logs
            emit('latest_server_logs', {"code": 200, "data": {"latest_server_logs": latest_logs_data}})
        else:
            # Emit WebSocket event indicating no server logs are available
            emit('latest_server_logs', {"code": 404, "message": "There are no server logs available."})
    except Exception as e:
        # Emit WebSocket event for error response
        emit('latest_server_logs', {"code": 500, "message": f"An error occurred: {str(e)}"})


if __name__ == "__main__":
    socketio.run(app, port=8000, debug=True)
    # app.run(port=8000, debug=True)

