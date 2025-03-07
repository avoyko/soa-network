from app.schemas import UserCreate, UserUpdate, UserLogin
from pydantic import ValidationError
import pytest

def test_user_create_schema_valid():
    # Тестируем валидные данные для создания пользователя
    user_data = {
        "login": "testuser",
        "password": "password123",
        "email": "test@example.com"
    }
    user = UserCreate(**user_data)
    assert user.login == "testuser"
    assert user.password == "password123"
    assert user.email == "test@example.com"

def test_user_create_schema_invalid_email():
    # Тестируем невалидный email
    user_data = {
        "login": "testuser",
        "password": "password123",
        "email": "invalid-email"  # Неверный формат email
    }
    
    with pytest.raises(ValidationError):
        UserCreate(**user_data)

def test_user_login_schema():
    # Тестируем схему логина
    login_data = {
        "login": "testuser",
        "password": "password123"
    }
    login = UserLogin(**login_data)
    assert login.login == "testuser"
    assert login.password == "password123"

def test_user_update_schema():
    # Тестируем схему обновления данных пользователя
    update_data = {
        "first_name": "John",
        "last_name": "Doe",
        "birth_date": "1990-01-01",
        "email": "new@example.com",
        "phone": "+1234567890",
        "bio": "Test bio"
    }
    update = UserUpdate(**update_data)
    assert update.first_name == "John"
    assert update.last_name == "Doe"
    assert update.birth_date.isoformat() == "1990-01-01"
    assert update.email == "new@example.com"
    assert update.phone == "+1234567890"

def test_user_update_schema_partial():
    # Тестируем частичное обновление данных пользователя
    update_data = {
        "first_name": "John",
        "last_name": "Doe"
    }
    update = UserUpdate(**update_data)
    assert update.first_name == "John"
    assert update.last_name == "Doe"
    assert update.birth_date is None
    assert update.email is None
    assert update.phone is None
