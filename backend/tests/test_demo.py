# import pytest
# from main import app

# @pytest.fixture
# def client():
#     app.config['TESTING'] = True
#     with app.test_client() as client:
#         yield client

# def test_request_example():
#     assert b"<h2>Hello, World!</h2>" == b"<h2>Hello, World!</h2>"


import pytest
import json
from main import app
from flask import Flask
from serverLogs.serverLogsService import serverLogsClass
from socketioMethods import socketioClass

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_server_logs(client):
    response = client.get('/serverlogs/server_logs')
    assert response.status_code == 200
    data = response.get_json()
    assert 'server_logs' in data['data']
    assert len(data['data']['server_logs']) > 0

def test_get_latest_server_logs(client):
    response = client.get('/serverlogs/server_logs/latest')
    assert response.status_code == 200
    data = response.get_json()
    assert 'latest_server_logs' in data['data']
    assert len(data['data']['latest_server_logs']) > 0


@pytest.fixture
def mock_query_all(mocker):
    # Mocking the query.all() method to return some dummy data
    return mocker.patch('db.session.query(ServerLogs).join().all', side_effect=[
        [
            {'InfrastructureName': '4.231.173.187:9100', 'ServerDiskUtilisation': 17.336145401000977, 'ServerCpuUtilisation': 0.46666666865348816, 'ServerAvailability': 1, 'LogDateTime': '2024-03-02 08:54:44', 'InfrastructureType': 'server', 'ServerMemoryUtilisation': 19.930654525756836, 'ServerNetworkAvailability': 1},
            {'InfrastructureName': '20.123.40.22', 'ServerDiskUtilisation': 7.985710144042969, 'ServerCpuUtilisation': 0.3505840003490448, 'ServerAvailability': 1, 'LogDateTime': '2024-03-02 09:02:20', 'InfrastructureType': 'server', 'ServerMemoryUtilisation': 26.69349479675293, 'ServerNetworkAvailability': 1},
            {'InfrastructureName': '4.231.170.13', 'ServerDiskUtilisation': 0.0, 'ServerCpuUtilisation': 0.0, 'ServerAvailability': 0, 'LogDateTime': '2024-03-02 09:02:20', 'InfrastructureType': 'server', 'ServerMemoryUtilisation': 0.0, 'ServerNetworkAvailability': 0},
            {'InfrastructureName': '4.231.171.90', 'ServerDiskUtilisation': 8.105874061584473, 'ServerCpuUtilisation': 0.3171420097351074, 'ServerAvailability': 1, 'LogDateTime': '2024-03-02 09:02:21', 'InfrastructureType': 'server', 'ServerMemoryUtilisation': 26.44856071472168, 'ServerNetworkAvailability': 1},
            {'InfrastructureName': '74.234.41.9', 'ServerDiskUtilisation': 0.0, 'ServerCpuUtilisation': 0.0, 'ServerAvailability': 0, 'LogDateTime': '2024-03-02 09:02:21', 'InfrastructureType': 'server', 'ServerMemoryUtilisation': 0.0, 'ServerNetworkAvailability': 0},
            {'InfrastructureName': '4.231.173.187:9100', 'ServerDiskUtilisation': 17.336145401000977, 'ServerCpuUtilisation': 0.46666666865348816, 'ServerAvailability': 1, 'LogDateTime': '2024-03-01 08:54:44', 'InfrastructureType': 'server', 'ServerMemoryUtilisation': 19.930654525756836, 'ServerNetworkAvailability': 1},
            {'InfrastructureName': '20.123.40.22', 'ServerDiskUtilisation': 7.985710144042969, 'ServerCpuUtilisation': 0.3505840003490448, 'ServerAvailability': 1, 'LogDateTime': '2024-03-01 09:02:20', 'InfrastructureType': 'server', 'ServerMemoryUtilisation': 26.69349479675293, 'ServerNetworkAvailability': 1},
            {'InfrastructureName': '4.231.170.13', 'ServerDiskUtilisation': 0.0, 'ServerCpuUtilisation': 0.0, 'ServerAvailability': 0, 'LogDateTime': '2024-03-01 09:02:20', 'InfrastructureType': 'server', 'ServerMemoryUtilisation': 0.0, 'ServerNetworkAvailability': 0},
            {'InfrastructureName': '4.231.171.90', 'ServerDiskUtilisation': 8.105874061584473, 'ServerCpuUtilisation': 0.3171420097351074, 'ServerAvailability': 1, 'LogDateTime': '2024-03-01 09:02:21', 'InfrastructureType': 'server', 'ServerMemoryUtilisation': 26.44856071472168, 'ServerNetworkAvailability': 1},
            {'InfrastructureName': '74.234.41.9', 'ServerDiskUtilisation': 0.0, 'ServerCpuUtilisation': 0.0, 'ServerAvailability': 0, 'LogDateTime': '2024-03-01 09:02:21', 'InfrastructureType': 'server', 'ServerMemoryUtilisation': 0.0, 'ServerNetworkAvailability': 0},
            {'InfrastructureName': '4.231.173.187:9100', 'ServerDiskUtilisation': 17.336145401000977, 'ServerCpuUtilisation': 0.46666666865348816, 'ServerAvailability': 1, 'LogDateTime': '2024-03-02 07:54:44', 'InfrastructureType': 'server', 'ServerMemoryUtilisation': 19.930654525756836, 'ServerNetworkAvailability': 1},
            {'InfrastructureName': '20.123.40.22', 'ServerDiskUtilisation': 7.985710144042969, 'ServerCpuUtilisation': 0.3505840003490448, 'ServerAvailability': 1, 'LogDateTime': '2024-03-02 08:02:20', 'InfrastructureType': 'server', 'ServerMemoryUtilisation': 26.69349479675293, 'ServerNetworkAvailability': 1},
            {'InfrastructureName': '4.231.170.13', 'ServerDiskUtilisation': 0.0, 'ServerCpuUtilisation': 0.0, 'ServerAvailability': 0, 'LogDateTime': '2024-03-02 08:02:20', 'InfrastructureType': 'server', 'ServerMemoryUtilisation': 0.0, 'ServerNetworkAvailability': 0},
            {'InfrastructureName': '4.231.171.90', 'ServerDiskUtilisation': 8.105874061584473, 'ServerCpuUtilisation': 0.3171420097351074, 'ServerAvailability': 1, 'LogDateTime': '2024-03-02 08:02:21', 'InfrastructureType': 'server', 'ServerMemoryUtilisation': 26.44856071472168, 'ServerNetworkAvailability': 1},
            {'InfrastructureName': '74.234.41.9', 'ServerDiskUtilisation': 0.0, 'ServerCpuUtilisation': 0.0, 'ServerAvailability': 0, 'LogDateTime': '2024-03-02 08:02:21', 'InfrastructureType': 'server', 'ServerMemoryUtilisation': 0.0, 'ServerNetworkAvailability': 0}
        ]
    ])

@pytest.fixture
def mock_metric_threshold():
    class MockMetricThreshold:
        def __init__(self, Metric, CriticalThreshold, BadThreshold, WarningThreshold):
            self.Metric = Metric
            self.CriticalThreshold = CriticalThreshold
            self.BadThreshold = BadThreshold
            self.WarningThreshold = WarningThreshold

    return MockMetricThreshold

# test_socketioClass.py


def test_query_database_for_new_records(mock_query_all):
    # Mocking necessary dependencies for the method
    # last_checked_timestamps = {'server1': '2024-03-01T12:00:00', 'server2': '2024-03-02T12:00:00'}

    # Call the method and check if it returns a list
    assert isinstance(socketioClass.query_database_for_new_records(), list)
    assert len(socketioClass.query_database_for_new_records()) > 0

    # Hardcoded expected latest log date time for each server
    expected_latest_log_date_times = {
        '4.231.173.187:9100': '2024-03-02 08:54:44',
        '20.123.40.22': '2024-03-02 09:02:20',
        '4.231.170.13': '2024-03-02 09:02:20',
        '4.231.171.90': '2024-03-02 09:02:21',
        '74.234.41.9': '2024-03-02 09:02:21'
    }

    # Check if the log date time is the latest for each server
    for server_data in socketioClass.query_database_for_new_records():
        server_name = server_data['InfrastructureName']
        log_date_time = server_data['LogDateTime']
        expected_log_date_time = expected_latest_log_date_times[server_name]
        assert log_date_time == expected_log_date_time


def test_get_historical_logs(mock_query_all):
    # Mocking necessary dependencies for the method
    start_time = '2024-03-02 07:00:00'
    end_time = '2024-03-02 10:00:00'

    # Call the method and check if it returns a list
    historical_logs = socketioClass.get_historical_logs(start_time, end_time)
    assert isinstance(historical_logs, list)

    # Check if the length of returned historical logs is as expected
    assert len(historical_logs) == 10

    # Check if each log entry has the expected keys
    expected_keys = [
        'InfrastructureName', 'ServerDiskUtilisation', 'ServerCpuUtilisation',
        'ServerAvailability', 'LogDateTime', 'InfrastructureType',
        'ServerMemoryUtilisation', 'ServerNetworkAvailability'
    ]
    for log_entry in historical_logs:
        assert all(key in log_entry for key in expected_keys)

    # Check if all LogDateTime entries are within the specified range
    for log_entry in historical_logs:
        assert start_time <= log_entry['LogDateTime'] <= end_time


def test_get_health_status_socket(mocker):
    # Mocking necessary dependencies for the method
    latest_server_logs = [
        {'InfrastructureName': '4.231.173.187:9100', 'ServerDiskUtilisation': 17.336145401000977, 'ServerCpuUtilisation': 0.46666666865348816, 'ServerAvailability': 1, 'LogDateTime': '2024-03-02 07:54:44', 'InfrastructureType': 'server', 'ServerMemoryUtilisation': 19.930654525756836, 'ServerNetworkAvailability': 1},
        {'InfrastructureName': '20.123.40.22', 'ServerDiskUtilisation': 7.985710144042969, 'ServerCpuUtilisation': 0.3505840003490448, 'ServerAvailability': 1, 'LogDateTime': '2024-03-02 08:02:20', 'InfrastructureType': 'server', 'ServerMemoryUtilisation': 26.69349479675293, 'ServerNetworkAvailability': 1},
        {'InfrastructureName': '4.231.170.13', 'ServerDiskUtilisation': 0.0, 'ServerCpuUtilisation': 0.0, 'ServerAvailability': 0, 'LogDateTime': '2024-03-02 08:02:20', 'InfrastructureType': 'server', 'ServerMemoryUtilisation': 0.0, 'ServerNetworkAvailability': 0},
        {'InfrastructureName': '4.231.171.90', 'ServerDiskUtilisation': 8.105874061584473, 'ServerCpuUtilisation': 0.3171420097351074, 'ServerAvailability': 1, 'LogDateTime': '2024-03-02 08:02:21', 'InfrastructureType': 'server', 'ServerMemoryUtilisation': 26.44856071472168, 'ServerNetworkAvailability': 1},
        {'InfrastructureName': '74.234.41.9', 'ServerDiskUtilisation': 0.0, 'ServerCpuUtilisation': 0.0, 'ServerAvailability': 0, 'LogDateTime': '2024-03-02 08:02:21', 'InfrastructureType': 'server', 'ServerMemoryUtilisation': 0.0, 'ServerNetworkAvailability': 0}
    ]

    # Mock the MetricThreshold.query.all() method to return some dummy data
    mocker.patch('MetricThreshold.query.all', return_value=[
        mock_metric_threshold(Metric='ServerAvailability', CriticalThreshold=0.0, BadThreshold=0.0, WarningThreshold=0.0),
        mock_metric_threshold(Metric='ServerCpuUtilisation', CriticalThreshold=90.0, BadThreshold=80.0, WarningThreshold=70.0),
        mock_metric_threshold(Metric='ServerDiskUtilisation', CriticalThreshold=90.0, BadThreshold=80.0, WarningThreshold=70.0),
        mock_metric_threshold(Metric='ServerMemoryUtilisation', CriticalThreshold=90.0, BadThreshold=80.0, WarningThreshold=70.0),
        mock_metric_threshold(Metric='ServerNetworkAvailability', CriticalThreshold=0.0, BadThreshold=0.0, WarningThreshold=0.0)
    ])

    # Call the method and check if it returns a JSON response
    response, status_code = socketioClass.get_health_status_socket(latest_server_logs)

    # Check if the response is as expected
    assert status_code == 200
    assert isinstance(response, dict)
    assert 'code' in response
    assert 'data' in response

    # Check if the 'data' field contains a list
    data = response['data']
    assert isinstance(data, list)

    # Check if each entry in the 'data' list has the expected keys
    for entry in data:
        expected_keys = ['InfrastructureName', 'InfrastructureType', 'LogDateTime', 'OverallHealthStatus', 'HealthStatus']
        assert all(key in entry for key in expected_keys)

