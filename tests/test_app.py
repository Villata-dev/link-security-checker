import pytest
import os
from unittest.mock import patch, MagicMock

# Set a dummy API key before importing the app to avoid 500 errors
os.environ["VT_API_KEY"] = "test_api_key"

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('app.requests.get')
def test_scan_url_safe(mock_get, client):
    # Mock VirusTotal API response for a safe URL
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": {
            "attributes": {
                "last_analysis_stats": {
                    "malicious": 0,
                    "suspicious": 0
                },
                "last_analysis_date": 1600000000
            }
        }
    }
    mock_get.return_value = mock_response

    response = client.post('/api/scan', json={"url": "https://google.com"})

    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'SAFE'
    assert data['malicious_count'] == 0
    assert "limpio" in data['message']

@patch('app.requests.get')
def test_scan_url_malicious(mock_get, client):
    # Mock VirusTotal API response for a malicious URL (5 engines detected)
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": {
            "attributes": {
                "last_analysis_stats": {
                    "malicious": 5,
                    "suspicious": 0
                },
                "last_analysis_date": 1600000000
            }
        }
    }
    mock_get.return_value = mock_response

    response = client.post('/api/scan', json={"url": "http://malicious-site.com"})

    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'DANGER'
    assert data['malicious_count'] == 5
    assert "Peligro" in data['message']
