import pytest
import httpx
import json
import time

@pytest.mark.asyncio
async def test_register_user(api_client):
    """Тест регистрации пользователя через API Gateway."""
    # Создаем уникальный логин с использованием timestamp
    timestamp = int(time.time())
    test_user = {
        "login": f"test_user_{timestamp}",
        "password": "password123",
        "email": f"test_{timestamp}@example.com"
    }
    
    # Отправляем запрос на регистрацию
    response = await api_client.post("/auth/register", json=test_user)
    
    # Проверяем ответ
    assert response.status_code == 201
    data = response.json()
    assert data["login"] == test_user["login"]
    assert data["email"] == test_user["email"]
    
    return test_user  # Возвращаем данные пользователя для использования в других тестах

@pytest.mark.asyncio
async def test_login_success(api_client):
    """Тест успешного входа в систему."""
    # Сначала регистрируем пользователя
    timestamp = int(time.time())
    test_user = {
        "login": f"test_user_{timestamp}",
        "password": "password123",
        "email": f"test_{timestamp}@example.com"
    }
    
    # Отправляем запрос на регистрацию
    response = await api_client.post("/auth/register", json=test_user)
    
    # Затем пробуем войти
    login_data = {
        "login": test_user["login"],
        "password": test_user["password"]
    }
    
    response = await api_client.post("/auth/login", json=login_data)
    
    # Проверяем ответ
    assert response.status_code == 200
    data = response.json()

@pytest.mark.asyncio
async def test_login_wrong_password(api_client):
    """Тест входа с неверным паролем."""
    # Сначала регистрируем пользователя
    timestamp = int(time.time())
    test_user = {
        "login": f"test_user_{timestamp}",
        "password": "password123",
        "email": f"test_{timestamp}@example.com"
    }
    
    # Отправляем запрос на регистрацию
    response = await api_client.post("/auth/register", json=test_user)
    
    # Затем пробуем войти с неверным паролем
    login_data = {
        "login": test_user["login"],
        "password": "wrong_password"
    }
    
    response = await api_client.post("/auth/login", json=login_data)
    
    # Проверяем ответ
    assert response.status_code == 401
    data = response.json()
    assert "Неверный логин или пароль" in data["detail"]

@pytest.mark.asyncio
async def test_get_profile(api_client):
    """Тест получения профиля пользователя."""
    # Сначала регистрируем пользователя
    timestamp = int(time.time())
    test_user = {
        "login": f"test_user_{timestamp}",
        "password": "password123",
        "email": f"test_{timestamp}@example.com"
    }
    
    # Отправляем запрос на регистрацию
    response = await api_client.post("/auth/register", json=test_user)
    
    # Затем получаем его профиль
    response = await api_client.get(f"/users/profile/{test_user['login']}")
    
    # Проверяем ответ
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_update_profile(api_client):
    """Тест обновления профиля пользователя."""
    # Сначала регистрируем пользователя
    timestamp = int(time.time())
    test_user = {
        "login": f"test_user_{timestamp}",
        "password": "password123",
        "email": f"test_{timestamp}@example.com"
    }
    
    # Отправляем запрос на регистрацию
    response = await api_client.post("/auth/register", json=test_user)
    
    # Данные для обновления
    update_data = {
        "first_name": "Test",
        "last_name": "User",
        "birth_date": "1990-01-01",
        "phone": "+1234567890",
        "bio": "Test bio"
    }
    
    # Отправляем запрос на обновление профиля
    response = await api_client.put(
        f"/users/profile/{test_user['login']}", 
        json=update_data
    )
    
    # Проверяем ответ
    assert response.status_code == 200
    data = response.json()
    assert data["login"] == test_user["login"]
    assert data["email"] == test_user["email"]
    assert data["first_name"] == update_data["first_name"]
    assert data["last_name"] == update_data["last_name"]
    assert data["birth_date"] == update_data["birth_date"]
    assert data["phone"] == update_data["phone"]
    
    # Проверяем, что данные действительно обновились, получив профиль
    response = await api_client.get(f"/users/profile/{test_user['login']}")
    data = response.json()
    assert data["first_name"] == update_data["first_name"]
    assert data["last_name"] == update_data["last_name"]

@pytest.mark.asyncio
async def test_nonexistent_profile(api_client):
    """Тест получения несуществующего профиля."""
    response = await api_client.get("/users/profile/nonexistent_user")
    
    # Проверяем, что получаем ошибку 404
    assert response.status_code == 404
    data = response.json()
    assert "Пользователь не найден" in data["detail"]
