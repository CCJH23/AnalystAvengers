import pytest
from main import app
import urllib.parse

# Set up the Flask app for testing
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_infrastructureconfig_records_sucess(client):
    response = client.get('/infrastructureconfig/infrastructure_config')
    response_data = response.json

    # assertions
    assert response.status_code == 200
    assert "server_configurations" in response_data["data"]
    assert "InfrastructureCountry" in response_data["data"]["server_configurations"][0]
    assert "InfrastructureName" in response_data["data"]["server_configurations"][0]
    assert "InfrastructurePriority" in response_data["data"]["server_configurations"][0]
    assert "InfrastructureType" in response_data["data"]["server_configurations"][0]
    assert "MonitoringTool" in response_data["data"]["server_configurations"][0]


def test_get_infrastructureconfig_records_by_name_sucess(client):
    infrastructureName = "Monitoring Linux Machine 1"
    urlEncodedInfrastructureName = urllib.parse.quote(infrastructureName)
    response = client.get('/infrastructureconfig/infrastructure_config/{}'.format(urlEncodedInfrastructureName))
    response_data = response.json

    # assertions
    assert response.status_code == 200
    assert "server_configuration" in response_data["data"]
    assert "InfrastructureCountry" in response_data["data"]["server_configuration"]
    assert "InfrastructureName" in response_data["data"]["server_configuration"]
    assert "InfrastructurePriority" in response_data["data"]["server_configuration"]
    assert "InfrastructureType" in response_data["data"]["server_configuration"]
    assert "MonitoringTool" in response_data["data"]["server_configuration"]
    assert response_data["data"]["server_configuration"]["InfrastructureName"] == infrastructureName

