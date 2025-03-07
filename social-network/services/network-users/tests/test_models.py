from datetime import date
from app.models import User
import pytest

def test_user_model_create(db):
    # Проверяем создание пользователя
    user = User(
        login="testuser1",
        password_hash="hashedpassword",
        email="test1@example.com",
        first_name="John",
        last_name="Doe",
        birth_date=date(1990, 1, 1),
        phone="+1234567890"
    )
    db.add(user)
    db.commit()
    
    # Получаем пользователя из БД
    db_user = db.query(User).filter(User.login == "testuser1").first()
    
    # Проверяем, что все поля сохранены правильно
    assert db_user.login == "testuser1"
    assert db_user.password_hash == "hashedpassword"
    assert db_user.email == "test1@example.com"
    assert db_user.first_name == "John"
    assert db_user.last_name == "Doe"
    assert db_user.birth_date == date(1990, 1, 1)
    assert db_user.phone == "+1234567890"
    
    # Проверяем, что даты созданы автоматически
    assert db_user.created_at is not None
    assert db_user.updated_at is not None

def test_user_model_update(db, test_user):
    # Проверяем обновление пользователя
    test_user.first_name = "Updated"
    test_user.last_name = "Name"
    db.commit()
    db.refresh(test_user)
    
    # Получаем пользователя из БД
    db_user = db.query(User).filter(User.login == "testuser").first()
    
    # Проверяем, что поля обновлены
    assert db_user.first_name == "Updated"
    assert db_user.last_name == "Name"
    
    # Проверяем, что дата обновления изменилась
    assert db_user.updated_at != db_user.created_at
