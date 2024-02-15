import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

if __name__ == '__main__':
    # Run all tests in the 'tests/' directory
    pytest.main(['tests/'])