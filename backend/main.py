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
from problemLogs.problemLogsController import problemLogsBp
from socketioMethods import socketioClass

# external imports
from dotenv import load_dotenv
import os
from flask import Flask
from flask_socketio import SocketIO, emit
from sqlalchemy import text, func, and_ #func is a module provided by SQLAlchemy that allows usage of SQL functions in queries. and_ is a logical operator provided by SQLAlchemy that constructs an SQL AND clause.
from flask_cors import CORS
import time, datetime, json
from threading import Thread
from datetime import datetime, timedelta
import pytz

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
app.register_blueprint(problemLogsBp)

################
# DEFAULT ROUTES
################
@app.route('/')
def hello_world():
    if check_db_connection():
        return "Connection to the database established!"
    else:
        return "Failed to connect to the database."


#########
# METHODS
#########
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


# socketio 
# Function to continuously poll the database for changes
def poll_database_for_changes():
    with app.app_context():
        # last_checked_timestamp = socketioClass.get_last_checked_timestamps()
        # print("Last Checked Timestamps:", last_checked_timestamp)
        while True:
            new_records = socketioClass.query_database_for_new_records()
            # print("New Records:", new_records)

            if new_records:
                socketio.emit('latest_server_logs', {"code": 200, "data": {"latest_server_logs": new_records}}, namespace='/latestlogs')

                # Execute the health check function based on new records
                response, status_code = socketioClass.get_health_status_socket(new_records)
                health_data = json.loads(response.data.decode('utf-8'))
                # print("Health Status Response:", health_data['data'])
                if status_code == 200:
                    socketio.emit('health_status', {"code": 200, "data": health_data['data']}, namespace='/latestlogs')
                else:
                    print("Health Status Check Failed. Status Code:", status_code)

            last_checked_timestamp = socketioClass.get_latest_timestamp(new_records)
            # print("Last Checked Timestamps:", last_checked_timestamp)
            socketioClass.update_last_checked_timestamps(last_checked_timestamp)
            
            time.sleep(10)  # Adjust the interval as needed

# Function to retrieve historical logs for each unique server within the past hour
def get_historical_logs():
    with app.app_context():
        while True:
            # Calculate time frame
            gmt = pytz.timezone('GMT')
            end_time = datetime.now(gmt)
            # end_time = datetime.now()
            start_time = end_time - timedelta(hours=1)

            # Retrieve historical logs for each unique server
            historical_logs = socketioClass.get_historical_logs(start_time, end_time)

            # print("Historical Logs:", historical_logs)
            # Emit historical logs to frontend
            socketio.emit('historical_server_logs', {"code": 200, "data": {"historical_server_logs": historical_logs}}, namespace='/latestlogs')

            time.sleep(10)

# Function to retrieve all problem logs 
def get_problem_logs():
    with app.app_context():
        while True:
            # retrieve all problem logs
            problem_logs = socketioClass.get_problem_logs()

            # print("ProblemLogs:", problem_logs)

            # Emit problem logs to frontend
            socketio.emit('problem_logs', {"code": 200, "data": {"problem_logs": problem_logs}}, namespace='/latestlogs')

            time.sleep(10)


@socketio.on('serverlog', namespace='/latestlogs')
def handle_server_logs_connect():
    pass  # No action required on client connection


if __name__ == "__main__":
    # Start the polling process in a separate thread
    polling_thread = Thread(target=poll_database_for_changes)
    polling_thread.daemon = True
    polling_thread.start()

    # Start the historical logs retrieval process in a separate thread
    historical_logs_thread = Thread(target=get_historical_logs)
    historical_logs_thread.daemon = True
    historical_logs_thread.start()

    # Start the problem logs retrieval process in a separate thread
    problem_logs_thread = Thread(target=get_problem_logs)
    problem_logs_thread.daemon = True
    problem_logs_thread.start()

    # Start the Flask-SocketIO server
    socketio.run(app, port=8000, debug=True)

