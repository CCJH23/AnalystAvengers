import pytest
from main import app

# Set up the Flask app for testing
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_serverlogs_records_success(client):
    response = client.get('/problemlogs/problem_logs')
    data = response.json

    # asserts
    assert response.status_code == 200
    assert 'problem_logs' in data['data']
    assert 'InfrastructureName' in data['data']['problem_logs'][0]
    assert 'LogDateTime' in data['data']['problem_logs'][0]
    assert 'ProblemName' in data['data']['problem_logs'][0]
    assert 'ProblemSeverity' in data['data']['problem_logs'][0]

