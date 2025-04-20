import pytest
import httpx
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import User
from app.routes import get_password_hash
import time
import pytest_asyncio


TEST_DB_URL = "sqlite:///./test.db"


@pytest.fixture(scope="session")
def engine():

    retries = 30
    for i in range(retries):
        try:
            print(f"Trying to connect to database (attempt {i+1}/{retries})...")

            temp_engine = create_engine(TEST_DB_URL)
            with temp_engine.connect() as conn:
                print("Database connection successful!")
                break
        except Exception as e:
            print(f"Database connection error: {e}")
            if i == retries - 1:
                raise
            time.sleep(2)

    connect_args = {}
    if TEST_DB_URL.startswith("sqlite"):
        connect_args = {"check_same_thread": False}

    engine = create_engine(TEST_DB_URL, connect_args=connect_args)

    print("Creating database tables...")
    Base.metadata.create_all(
        bind=engine,
    )

    yield engine

    print("Dropping database tables...")
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(engine):

    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def users_service_url():

    return "http://localhost:8000"


@pytest_asyncio.fixture
async def users_client():

    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        yield client


@pytest.fixture
def test_user(db_session):

    user = User(
        login="test_user",
        password_hash=get_password_hash("test_password"),
        email="test@example.com",
        first_name="Test",
        last_name="User",
    )
    db_session.add(user)
    db_session.commit()
    yield user
    db_session.delete(user)
    db_session.commit()
