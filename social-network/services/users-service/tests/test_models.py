import pytest
from app.models import User
from datetime import date, datetime, timezone
import time


def test_user_model_create(db_session):
    timestamp = int(time.time())
    user = User(
        login=f"model_test_user_{timestamp}",
        password_hash="hashed_password",
        email=f"model_test_{timestamp}@example.com",
        first_name="Test",
        last_name="User",
        birth_date=date(1990, 1, 1),
        phone="+1234567890",
    )

    db_session.add(user)
    db_session.commit()

    db_user = db_session.query(User).filter(User.login == user.login).first()

    assert db_user is not None
    assert db_user.login == user.login
    assert db_user.password_hash == "hashed_password"
    assert db_user.email == user.email
    assert db_user.first_name == "Test"
    assert db_user.last_name == "User"
    assert db_user.birth_date == date(1990, 1, 1)
    assert db_user.phone == "+1234567890"
    assert db_user.created_at is not None
    assert db_user.updated_at is not None

    db_session.delete(db_user)
    db_session.commit()


def test_user_model_update(db_session, test_user):

    original_updated_at = test_user.updated_at

    time.sleep(1)

    test_user.first_name = "Updated"
    test_user.last_name = "Name"
    test_user.birth_date = date(1995, 5, 5)

    db_session.commit()
    db_session.refresh(test_user)

    assert test_user.first_name == "Updated"
    assert test_user.last_name == "Name"
    assert test_user.birth_date == date(1995, 5, 5)

    assert test_user.updated_at > original_updated_at


def test_user_model_fields(db_session):

    timestamp = int(time.time())
    user = User(
        login=f"full_user_{timestamp}",
        password_hash="full_hashed_password",
        email=f"full_{timestamp}@example.com",
        first_name="Full",
        last_name="User",
        birth_date=date(1985, 12, 31),
        phone="+9876543210",
    )

    db_session.add(user)
    db_session.commit()

    db_user = db_session.query(User).filter(User.login == user.login).first()

    assert db_user.login == user.login
    assert db_user.password_hash == user.password_hash
    assert db_user.email == user.email
    assert db_user.first_name == user.first_name
    assert db_user.last_name == user.last_name
    assert db_user.birth_date == user.birth_date
    assert db_user.phone == user.phone
    assert db_user.created_at is not None
    assert db_user.updated_at is not None

    db_session.delete(db_user)
    db_session.commit()
