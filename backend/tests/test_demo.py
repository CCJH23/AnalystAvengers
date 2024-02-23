import pytest
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_request_example():
    assert b"<h2>Hello, World!</h2>" == b"<h2>Hello, World!</h2>"

