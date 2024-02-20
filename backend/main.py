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

