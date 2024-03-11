import pytest
from main import app

# Set up the Flask app for testing
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_metric_threshold(client):
    # fetch metric threshold from MetricThreshold table to see if correct response
    response = client.get('/metricthreshold/metricthresholds')
    response_data = response.json

    # assertions
    assert response.status_code == 200

    # check for example, the ServerAvailability metric has the correct thresholds
    assert response_data["ServerAvailability"] == [0.0, 0.0, 0.0]

