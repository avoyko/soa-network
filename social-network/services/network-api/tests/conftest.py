import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_httpx_client():
    with patch('app.httpx.AsyncClient') as mock_client:
        # Создаем мок объект для AsyncClient
        mock_instance = MagicMock()
        mock_client.return_value.__aenter__.return_value = mock_instance
        yield mock_instance
