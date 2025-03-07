import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.routes import get_password_hash

# Создаем тестовую БД в памяти
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    
    # Используем соединение с БД в тестах
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        # После каждого теста очищаем таблицы
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    # Переопределяем зависимость для использования тестовой БД
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    # Сбрасываем override после использования
    app.dependency_overrides = {}

@pytest.fixture(scope="function")
def test_user(db):
    # Создаем тестового пользователя
    from app.models import User
    
    user = User(
        login="testuser",
        password_hash=get_password_hash("testpassword"),
        email="test@example.com",
        first_name="Test",
        last_name="User"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
