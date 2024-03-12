import pytest
from main import app

# Set up the Flask app for testing
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_webapplogs_records_success(client):
    response = client.get('/webapplogs/web_app_logs')
    response_data = response.json

    # assertions
    assert response.status_code == 200
    assert "web_app_logs" in response_data["data"]
    assert "InfrastructureName" in response_data["data"]["web_app_logs"][0]
    assert "InfrastructureType" in response_data["data"]["web_app_logs"][0]
    assert "LogDateTime" in response_data["data"]["web_app_logs"][0]
    assert "WebAppAvailability" in response_data["data"]["web_app_logs"][0]
    assert "WebAppDuration" in response_data["data"]["web_app_logs"][0]
    assert "WebAppError" in response_data["data"]["web_app_logs"][0]
    assert "WebAppRate" in response_data["data"]["web_app_logs"][0]

