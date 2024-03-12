from main import app
from socketioMethods import socketioClass
from datetime import datetime, timedelta
import pytz
import json

def test_query_database_for_new_records_success():
    with app.app_context():
        new_serverlogs_records = socketioClass.query_database_for_new_serverlogs_records()
        first_record = new_serverlogs_records[0]

        # assertions
        assert "InfrastructureName" in first_record
        assert "InfrastructureType" in first_record
        assert "LogDateTime" in first_record
        assert "ServerCpuUtilisation" in first_record
        assert "ServerDiskUtilisation" in first_record
        assert "ServerMemoryUtilisation" in first_record
        assert "ServerNetworkAvailability" in first_record
        assert "ServerAvailability" in first_record

def test_get_health_status_socket_success():
    with app.app_context():
        new_serverlogs_records = socketioClass.query_database_for_new_serverlogs_records()
        response, status_code = socketioClass.get_health_status_socket(new_serverlogs_records)
        health_data_json = json.loads(response.data.decode('utf-8'))
        health_data = health_data_json['data']
        first_health_data_record = health_data[0]
        first_health_data_record_status = first_health_data_record["HealthStatus"]

        # assertions
        assert status_code == 200
        assert "InfrastructureName" in first_health_data_record
        assert "InfrastructureType" in first_health_data_record
        assert "LogDateTime" in first_health_data_record
        assert "OverallHealthStatus" in first_health_data_record
        assert "ServerAvailability" in first_health_data_record_status
        assert "ServerCpuUtilisation" in first_health_data_record_status
        assert "ServerDiskUtilisation" in first_health_data_record_status
        assert "ServerMemoryUtilisation" in first_health_data_record_status
        assert "ServerNetworkAvailability" in first_health_data_record_status


def test_get_historical_serverlogs_records_sucess():
    with app.app_context():
        # Calculate time frame
        gmt = pytz.timezone('GMT')
        end_time = datetime.now(gmt)
        start_time = end_time - timedelta(days=2)

        historical_serverlogs_records = socketioClass.get_historical_serverlogs_records(start_time, end_time)
        first_record = historical_serverlogs_records[0]

        # assertions
        assert "InfrastructureName" in first_record
        assert "InfrastructureType" in first_record
        assert "LogDateTime" in first_record
        assert "ServerCpuUtilisation" in first_record
        assert "ServerDiskUtilisation" in first_record
        assert "ServerMemoryUtilisation" in first_record
        assert "ServerNetworkAvailability" in first_record
        assert "ServerAvailability" in first_record

