import pytest
import httpx
import time

@pytest.mark.asyncio
async def test_register_user(users_client):
    """Тест регистрации пользователя."""
    timestamp = int(time.time())
    test_user = {
        "login": f"route_test_user_{timestamp}",
        "password": "password123",
        "email": f"route_test_{timestamp}@example.com"
    }
    
    response = await users_client.post("/auth/register", json=test_user)
    
    assert response.status_code == 201
    data = response.json()
    assert data["login"] == test_user["login"]
    assert data["email"] == test_user["email"]
    
    return test_user

@pytest.mark.asyncio
async def test_login(users_client):
    """Тест входа в систему."""
    # Регистрируем пользователя
    timestamp = int(time.time())
    test_user = {
        "login": f"route_test_user_{timestamp}",
        "password": "password123",
        "email": f"route_test_{timestamp}@example.com"
    }
    
    response = await users_client.post("/auth/register", json=test_user)
    data = response.json()
    # Входим в систему
    login_data = {
        "login": test_user["login"],
        "password": test_user["password"]
    }
    
    response = await users_client.post("/auth/login", json=login_data)
    
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_login_wrong_password(users_client):
    """Тест входа с неверным паролем."""
    # Регистрируем пользователя
    timestamp = int(time.time())
    test_user = {
        "login": f"route_test_user_{timestamp}",
        "password": "password123",
        "email": f"route_test_{timestamp}@example.com"
    }
    
    response = await users_client.post("/auth/register", json=test_user)
    # Пытаемся войти с неверным паролем
    login_data = {
        "login": test_user["login"],
        "password": "wrong_password"
    }
    
    response = await users_client.post("/auth/login", json=login_data)
    
    assert response.status_code == 401
    data = response.json()
    assert "Неверный логин или пароль" in data["detail"]

@pytest.mark.asyncio
async def test_get_profile(users_client):
    """Тест получения профиля."""
    # Регистрируем пользователя
    timestamp = int(time.time())
    test_user = {
        "login": f"route_test_user_{timestamp}",
        "password": "password123",
        "email": f"route_test_{timestamp}@example.com"
    }
    
    response = await users_client.post("/auth/register", json=test_user)
    
    # Получаем профиль
    response = await users_client.get(f"/users/profile/{test_user['login']}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["login"] == test_user["login"]
    assert data["email"] == test_user["email"]

@pytest.mark.asyncio
async def test_update_profile(users_client):
    """Тест обновления профиля."""
    # Регистрируем пользователя
    timestamp = int(time.time())
    test_user = {
        "login": f"route_test_user_{timestamp}",
        "password": "password123",
        "email": f"route_test_{timestamp}@example.com"
    }
    
    response = await users_client.post("/auth/register", json=test_user)
    
    # Обновляем профиль
    update_data = {
        "first_name": "Updated",
        "last_name": "User",
        "birth_date": "1990-01-01",
        "phone": "+1234567890"
    }
    
    response = await users_client.put(
        f"/users/profile/{test_user['login']}", 
        json=update_data
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["login"] == test_user["login"]
    assert data["email"] == test_user["email"]
    assert data["first_name"] == update_data["first_name"]
    assert data["last_name"] == update_data["last_name"]
    assert data["birth_date"] == update_data["birth_date"]
    assert data["phone"] == update_data["phone"]

@pytest.mark.asyncio
async def test_nonexistent_profile(users_client):
    """Тест получения несуществующего профиля."""
    timestamp = int(time.time())
    response = await users_client.get(f"/users/profile/nonexistent_user_{timestamp}")
    
    assert response.status_code == 404
    data = response.json()
    assert "Пользователь не найден" in data["detail"]
