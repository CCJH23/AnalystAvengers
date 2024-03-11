import pytest
from main import app

# Set up the Flask app for testing
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_serverlogs_records_success(client):
    response = client.get('/serverlogs/server_logs')
    data = response.json

    # asserts
    assert response.status_code == 200
    assert 'server_logs' in data['data']
    assert len(data['data']['server_logs']) > 0


def test_get_latest_serverlogs_records_success(client):
    response = client.get('/serverlogs/server_logs/latest')
    print(response)
    data = response.json

    # asserts
    assert response.status_code == 200
    assert 'latest_server_logs' in data['data']
    assert len(data['data']['latest_server_logs']) > 0

