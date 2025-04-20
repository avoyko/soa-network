import pytest
import pytest_asyncio
import os
import time
import asyncio
import grpc
import grpc.aio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from uuid import uuid4

# Импортируем Base из правильного места
from app.database import Base
from app.models import Post, Tag
from app.service import PostsService
from proto import posts_pb2, posts_pb2_grpc

# Используем in-memory SQLite для тестов
TEST_DB_URL = "sqlite:///:memory:"
# Адрес gRPC сервиса
GRPC_SERVICE_URL = "0.0.0.0:50051"




@pytest.fixture(scope="session")
def engine():
    """Создание движка SQLAlchemy для тестовой БД."""
    engine = create_engine(TEST_DB_URL)
    
    # Создаем таблицы
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # Удаляем таблицы
    print("Dropping database tables...")
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(engine):
    """Создание сессии БД для тестов."""
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Начинаем транзакцию для изоляции каждого теста
    session.begin_nested()
    
    yield session
    
    # Откатываем изменения после теста
    session.rollback()
    session.close()


@pytest.fixture
def posts_service(db_session):
    """Создание экземпляра PostsService для тестов."""
    return PostsService(db=db_session)


@pytest.fixture
def sample_tag(db_session):
    """Создание тестового тега в БД."""
    tag = Tag(name=f"test-tag-{uuid4()}")
    db_session.add(tag)
    db_session.commit()
    db_session.flush()
    
    yield tag


@pytest.fixture
def sample_post(db_session, sample_tag):
    """Создание тестового поста в БД."""
    post = Post(
        title="Test Post",
        description="This is a test post description",
        creator_id="test-user-id",
        is_private=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    post.tags = [sample_tag]
    db_session.add(post)
    db_session.commit()
    db_session.flush()
    
    yield post


@pytest.fixture
def private_post(db_session):
    """Создание приватного тестового поста в БД."""
    post = Post(
        title="Private Post",
        description="This is a private test post",
        creator_id="test-user-id",
        is_private=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db_session.add(post)
    db_session.commit()
    db_session.flush()
    
    yield post


@pytest_asyncio.fixture
async def grpc_channel():
    """Создание асинхронного канала gRPC для интеграционных тестов."""
    print(f"Connecting to gRPC service at {GRPC_SERVICE_URL}...")
    
    # Создаем асинхронный канал
    channel = grpc.aio.insecure_channel(GRPC_SERVICE_URL)
    
    # Проверяем соединение
    try:
        await asyncio.wait_for(channel.channel_ready(), timeout=5)
        print("Successfully connected to gRPC service!")
    except asyncio.TimeoutError:
        print(f"Warning: Timeout connecting to gRPC service at {GRPC_SERVICE_URL}")
        # Не вызываем fail, так как это только предупреждение
    
    yield channel
    
    # Закрываем канал после тестов
    await channel.close()


@pytest_asyncio.fixture
async def posts_stub(grpc_channel):
    return posts_pb2_grpc.PostsServiceStub(grpc_channel)
