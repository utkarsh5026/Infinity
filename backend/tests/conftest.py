"""
Pytest configuration and fixtures for testing
"""
import asyncio
from typing import AsyncGenerator, Generator
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool

from app.main import app
from app.config.database import Base, get_db
from app.config import settings
from app.models.user import User
from app.core.security import get_password_hash


# Override database URL for testing
TEST_DATABASE_URL = settings.TEST_DATABASE_URL or settings.DATABASE_URL.replace(
    "infinity_db", "infinity_test_db"
)


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """
    Create an event loop for the test session.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def test_db_engine():
    """
    Create a test database engine with NullPool for testing.
    Each test gets a fresh connection.
    """
    engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=NullPool,
        echo=False,
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Drop all tables after tests
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def test_db(test_db_engine) -> AsyncGenerator[AsyncSession, None]:
    """
    Create a test database session for each test.
    Automatically rolls back after each test.
    """
    # Create a new session factory
    async_session = async_sessionmaker(
        test_db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def client(test_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Create a test client with database session override.
    """
    # Override the get_db dependency
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    # Create test client
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac

    # Clear dependency overrides
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(test_db: AsyncSession) -> User:
    """
    Create a test user in the database.
    """
    user = User(
        email="test@example.com",
        username="testuser",
        full_name="Test User",
        hashed_password=get_password_hash("testpassword123"),
        is_active=True,
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user


@pytest_asyncio.fixture
async def test_user_2(test_db: AsyncSession) -> User:
    """
    Create a second test user for multi-user scenarios.
    """
    user = User(
        email="test2@example.com",
        username="testuser2",
        full_name="Test User 2",
        hashed_password=get_password_hash("testpassword456"),
        is_active=True,
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user


@pytest_asyncio.fixture
async def authenticated_client(client: AsyncClient, test_user: User) -> AsyncClient:
    """
    Create an authenticated test client with a valid access token.
    """
    # Login to get token
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": test_user.email,
            "password": "testpassword123"
        }
    )

    token_data = response.json()
    access_token = token_data["access_token"]

    # Set the authorization header
    client.headers["Authorization"] = f"Bearer {access_token}"

    return client


@pytest.fixture
def sample_user_data() -> dict:
    """
    Sample user data for registration tests.
    """
    return {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "newpassword123",
        "full_name": "New User"
    }


@pytest.fixture
def sample_login_data() -> dict:
    """
    Sample login credentials.
    """
    return {
        "email": "test@example.com",
        "password": "testpassword123"
    }
