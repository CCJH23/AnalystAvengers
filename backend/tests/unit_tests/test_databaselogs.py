import pytest
from main import app

# Set up the Flask app for testing
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_databaselogs_records_success(client):
    response = client.get('/databaselogs/database_logs')
    response_data = response.json

    # assertions
    assert response.status_code == 200
    assert "database_server_logs" in response_data["data"]
    assert "DatabaseAvailability" in response_data["data"]["database_server_logs"][0]
    assert "DatabaseAvailableConnections" in response_data["data"]["database_server_logs"][0]
    assert "DatabaseSlowQueryRate" in response_data["data"]["database_server_logs"][0]
    assert "DatabaseUptime" in response_data["data"]["database_server_logs"][0]
    assert "InfrastructureName" in response_data["data"]["database_server_logs"][0]
    assert "InfrastructureType" in response_data["data"]["database_server_logs"][0]
    assert "LogDateTime" in response_data["data"]["database_server_logs"][0]

