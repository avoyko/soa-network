import json
from fastapi import status
from unittest.mock import MagicMock

def test_proxy_register(client, mock_httpx_client):
    # Мокируем ответ от сервиса пользователей
    mock_response = MagicMock()
    mock_response.status_code = status.HTTP_201_CREATED
    mock_response.content = json.dumps({
        "login": "newuser",
        "email": "new@example.com",
        "created_at": "2023-01-01T00:00:00.000000",
        "updated_at": "2023-01-01T00:00:00.000000"
    }).encode()
    mock_response.headers = {"Content-Type": "application/json"}
    
    mock_httpx_client.request.return_value = mock_response
    
    # Выполняем запрос через API Gateway
    response = client.post(
        "/auth/register",
        json={
            "login": "newuser",
            "password": "password123",
            "email": "new@example.com"
        }
    )
    
    # Проверяем, что запрос был проксирован
    mock_httpx_client.request.assert_called_once()
    
    # Проверяем ответ
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["login"] == "newuser"
    assert data["email"] == "new@example.com"

def test_proxy_login(client, mock_httpx_client):
    # Мокируем ответ от сервиса пользователей
    mock_response = MagicMock()
    mock_response.status_code = status.HTTP_200_OK
    mock_response.content = json.dumps({
        "status": "success",
        "message": "Аутентификация успешна",
        "login": "testuser"
    }).encode()
    mock_response.headers = {"Content-Type": "application/json"}
    
    mock_httpx_client.request.return_value = mock_response
    
    # Выполняем запрос через API Gateway
    response = client.post(
        "/auth/login",
        json={
            "login": "testuser",
            "password": "testpassword"
        }
    )
    
    # Проверяем, что запрос был проксирован
    mock_httpx_client.request.assert_called_once()
    
    # Проверяем ответ
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "success"
    assert data["login"] == "testuser"

def test_proxy_get_profile(client, mock_httpx_client):
    # Мокируем ответ от сервиса пользователей
    mock_response = MagicMock()
    mock_response.status_code = status.HTTP_200_OK
    mock_response.content = json.dumps({
        "login": "testuser",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "created_at": "2023-01-01T00:00:00.000000",
        "updated_at": "2023-01-01T00:00:00.000000"
    }).encode()
    mock_response.headers = {"Content-Type": "application/json"}
    
    mock_httpx_client.request.return_value = mock_response
    
    # Выполняем запрос через API Gateway
    response = client.get("/users/profile/testuser")
    
    # Проверяем, что запрос был проксирован
    mock_httpx_client.request.assert_called_once()
    
    # Проверяем ответ
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["login"] == "testuser"
    assert data["email"] == "test@example.com"
    assert data["first_name"] == "Test"
    assert data["last_name"] == "User"

def test_proxy_update_profile(client, mock_httpx_client):
    # Мокируем ответ от сервиса пользователей
    mock_response = MagicMock()
    mock_response.status_code = status.HTTP_200_OK
    mock_response.content = json.dumps({
        "login": "testuser",
        "email": "test@example.com",
        "first_name": "Updated",
        "last_name": "Name",
        "birth_date": "1995-05-15",
        "phone": "+9876543210",
        "created_at": "2023-01-01T00:00:00.000000",
        "updated_at": "2023-01-02T00:00:00.000000"
    }).encode()
    mock_response.headers = {"Content-Type": "application/json"}
    
    mock_httpx_client.request.return_value = mock_response
    
    # Выполняем запрос через API Gateway
    response = client.put(
        "/users/profile/testuser",
        json={
            "first_name": "Updated",
            "last_name": "Name",
            "birth_date": "1995-05-15",
            "phone": "+9876543210"
        }
    )
    
    # Проверяем, что запрос был проксирован
    mock_httpx_client.request.assert_called_once()
    
    # Проверяем ответ
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["login"] == "testuser"
    assert data["first_name"] == "Updated"
    assert data["last_name"] == "Name"
    assert data["birth_date"] == "1995-05-15"
    assert data["phone"] == "+9876543210"

def test_proxy_error(client, mock_httpx_client):
    # Мокируем ответ с ошибкой от сервиса пользователей
    mock_response = MagicMock()
    mock_response.status_code = status.HTTP_404_NOT_FOUND
    mock_response.content = json.dumps({
        "detail": "Пользователь не найден"
    }).encode()
    mock_response.headers = {"Content-Type": "application/json"}
    
    mock_httpx_client.request.return_value = mock_response
    
    # Выполняем запрос через API Gateway
    response = client.get("/users/profile/nonexistentuser")
    
    # Проверяем, что запрос был проксирован
    mock_httpx_client.request.assert_called_once()
    
    # Проверяем ответ
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data["detail"] == "Пользователь не найден"
