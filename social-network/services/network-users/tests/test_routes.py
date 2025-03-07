from fastapi import status
import json
from datetime import date

def test_register_user(client):
    # Тестируем регистрацию пользователя
    response = client.post(
        "/auth/register",
        json={
            "login": "newuser",
            "password": "password123",
            "email": "new@example.com"
        }
    )
    
    # Проверяем статус и содержимое ответа
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["login"] == "newuser"
    assert data["email"] == "new@example.com"
    assert "password_hash" not in data

def test_register_duplicate_login(client, test_user):
    # Тестируем проверку на дублирование логина
    response = client.post(
        "/auth/register",
        json={
            "login": "testuser",  # Такой логин уже существует
            "password": "newpassword",
            "email": "another@example.com"
        }
    )
    
    # Проверяем статус и сообщение об ошибке
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Пользователь с таким логином уже существует" in response.text

def test_register_duplicate_email(client, test_user):
    # Тестируем проверку на дублирование email
    response = client.post(
        "/auth/register",
        json={
            "login": "newuser",
            "password": "password123",
            "email": "test@example.com"  # Такой email уже существует
        }
    )
    
    # Проверяем статус и сообщение об ошибке
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Пользователь с таким email уже существует" in response.text

def test_login_success(client, test_user):
    # Тестируем успешный логин
    response = client.post(
        "/auth/login",
        json={
            "login": "testuser",
            "password": "testpassword"
        }
    )
    
    # Проверяем статус и сообщение об успехе
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "success"
    assert data["login"] == "testuser"

def test_login_wrong_password(client, test_user):
    # Тестируем логин с неверным паролем
    response = client.post(
        "/auth/login",
        json={
            "login": "testuser",
            "password": "wrongpassword"
        }
    )
    
    # Проверяем статус и сообщение об ошибке
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Неверный логин или пароль" in response.text

def test_login_nonexistent_user(client):
    # Тестируем логин несуществующего пользователя
    response = client.post(
        "/auth/login",
        json={
            "login": "nonexistentuser",
            "password": "password123"
        }
    )
    
    # Проверяем статус и сообщение об ошибке
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Неверный логин или пароль" in response.text

def test_get_profile(client, test_user):
    # Тестируем получение профиля
    response = client.get(f"/users/profile/{test_user.login}")
    
    # Проверяем статус и содержимое ответа
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["login"] == test_user.login
    assert data["email"] == test_user.email
    assert data["first_name"] == test_user.first_name
    assert data["last_name"] == test_user.last_name

def test_get_nonexistent_profile(client):
    # Тестируем получение несуществующего профиля
    response = client.get("/users/profile/nonexistentuser")
    
    # Проверяем статус и сообщение об ошибке
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Пользователь не найден" in response.text

def test_update_profile(client, test_user):
    # Тестируем обновление профиля
    response = client.put(
        f"/users/profile/{test_user.login}",
        json={
            "first_name": "Updated",
            "last_name": "User",
            "birth_date": "1995-05-15",
            "phone": "+9876543210",
            "bio": "Test bio"
        }
    )
    
    # Проверяем статус и содержимое ответа
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["first_name"] == "Updated"
    assert data["last_name"] == "User"
    assert data["birth_date"] == "1995-05-15"
    assert data["phone"] == "+9876543210"
    assert data["bio"] == "Test bio"
    
    # Проверяем, что логин и email не изменились
    assert data["login"] == test_user.login
    assert data["email"] == test_user.email

def test_update_nonexistent_profile(client):
    # Тестируем обновление несуществующего профиля
    response = client.put(
        "/users/profile/nonexistentuser",
        json={
            "first_name": "Updated",
            "last_name": "User"
        }
    )
    
    # Проверяем статус и сообщение об ошибке
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Пользователь не найден" in response.text
