"""
Helper functions and utilities for testing
"""
from typing import Dict, Any, Optional
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.core.security import get_password_hash


async def create_test_user(
    db: AsyncSession,
    email: str = "testhelper@example.com",
    username: str = "testhelperuser",
    password: str = "testhelperpass",
    full_name: str = "Test Helper User",
    is_active: bool = True,
    **kwargs
) -> User:
    """
    Helper function to create a test user with custom attributes.

    Args:
        db: Database session
        email: User email
        username: Username
        password: Plain text password (will be hashed)
        full_name: User's full name
        is_active: Whether user is active
        **kwargs: Additional user attributes

    Returns:
        Created User object
    """
    user = User(
        email=email,
        username=username,
        full_name=full_name,
        hashed_password=get_password_hash(password),
        is_active=is_active,
        **kwargs
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_auth_token(
    client: AsyncClient,
    email: str,
    password: str
) -> Dict[str, str]:
    """
    Helper function to get authentication tokens.

    Args:
        client: Test client
        email: User email
        password: User password

    Returns:
        Dictionary with access_token, refresh_token, and token_type
    """
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password}
    )

    if response.status_code != 200:
        raise ValueError(f"Login failed with status {response.status_code}: {response.text}")

    return response.json()


async def get_auth_headers(
    client: AsyncClient,
    email: str,
    password: str
) -> Dict[str, str]:
    """
    Helper function to get authorization headers.

    Args:
        client: Test client
        email: User email
        password: User password

    Returns:
        Dictionary with Authorization header
    """
    token_data = await get_auth_token(client, email, password)
    return {"Authorization": f"Bearer {token_data['access_token']}"}


def assert_user_response(
    response_data: Dict[str, Any],
    expected_email: str,
    expected_username: str,
    expected_full_name: Optional[str] = None
):
    """
    Assert that a user response has the expected structure and values.

    Args:
        response_data: User response data from API
        expected_email: Expected email
        expected_username: Expected username
        expected_full_name: Expected full name (optional)
    """
    assert "id" in response_data
    assert response_data["email"] == expected_email
    assert response_data["username"] == expected_username

    if expected_full_name:
        assert response_data["full_name"] == expected_full_name

    # Ensure sensitive data is not exposed
    assert "hashed_password" not in response_data
    assert "password" not in response_data

    # Check standard fields
    assert "is_active" in response_data
    assert "created_at" in response_data
    assert "updated_at" in response_data


def assert_error_response(
    response_data: Dict[str, Any],
    expected_detail: Optional[str] = None
):
    """
    Assert that an error response has the expected structure.

    Args:
        response_data: Error response data from API
        expected_detail: Expected detail message (optional, checks substring)
    """
    assert "detail" in response_data

    if expected_detail:
        assert expected_detail.lower() in response_data["detail"].lower()


def assert_token_response(response_data: Dict[str, Any]):
    """
    Assert that a token response has the expected structure.

    Args:
        response_data: Token response data from API
    """
    assert "access_token" in response_data
    assert "refresh_token" in response_data
    assert "token_type" in response_data
    assert "expires_in" in response_data

    assert response_data["token_type"] == "bearer"
    assert isinstance(response_data["access_token"], str)
    assert isinstance(response_data["refresh_token"], str)
    assert len(response_data["access_token"]) > 0
    assert len(response_data["refresh_token"]) > 0

    # JWT tokens should have 3 parts
    assert len(response_data["access_token"].split(".")) == 3
    assert len(response_data["refresh_token"].split(".")) == 3


async def cleanup_user(db: AsyncSession, email: str):
    """
    Helper function to clean up a test user by email.

    Args:
        db: Database session
        email: User email to delete
    """
    from sqlalchemy import delete
    await db.execute(delete(User).where(User.email == email))
    await db.commit()


class TestDataFactory:
    """Factory for creating test data"""

    @staticmethod
    def user_data(
        email: str = "factory@example.com",
        username: str = "factoryuser",
        password: str = "factorypass123",
        full_name: str = "Factory User",
        **kwargs
    ) -> Dict[str, Any]:
        """Generate user registration data"""
        return {
            "email": email,
            "username": username,
            "password": password,
            "full_name": full_name,
            **kwargs
        }

    @staticmethod
    def login_data(
        email: str = "factory@example.com",
        password: str = "factorypass123"
    ) -> Dict[str, str]:
        """Generate login credentials"""
        return {
            "email": email,
            "password": password
        }

    @staticmethod
    def invalid_email_data() -> Dict[str, Any]:
        """Generate user data with invalid email"""
        return {
            "email": "not-an-email",
            "username": "testuser",
            "password": "testpass123",
            "full_name": "Test User"
        }

    @staticmethod
    def weak_password_data() -> Dict[str, Any]:
        """Generate user data with weak password"""
        return {
            "email": "test@example.com",
            "username": "testuser",
            "password": "123",  # Too short
            "full_name": "Test User"
        }
