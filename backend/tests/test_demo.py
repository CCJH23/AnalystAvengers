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
            {'InfrastructureName': '74.234.41.9', 'ServerDiskUtilisation': 0.0, 'ServerCpuUtilisation': 0.0, 'ServerAvailability': 0, 'LogDateTime': '2024-03-01 09:02:21', 'InfrastructureType': 'server', 'ServerMemoryUtilisation': 0.0, 'ServerNetworkAvailability': 0}
        ]
    ])


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


def test_get_historical_logs():
    # Mocking necessary dependencies for the method
    start_time = '2024-03-01 00:00:00'
    end_time = '2024-03-01 23:59:59'

    # Call the method and check if it returns a list
    assert isinstance(socketioClass.get_historical_logs(start_time, end_time), list)

def test_get_health_status_socket():
    # Mocking necessary dependencies for the method
    latest_server_logs = [{'InfrastructureName': 'server1', 'InfrastructureType': 'type1', 'LogDateTime': '2024-03-01 12:00:00', 'metric1': 80}]

    # Call the method and check if it returns a JSON response
    response = socketioClass.get_health_status_socket(latest_server_logs)
    assert isinstance(response, tuple)  # Check if it's a tuple
    assert len(response) == 2  # Check if it contains both status code and data
