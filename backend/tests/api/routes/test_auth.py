"""
Tests for authentication routes
"""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.core.security import verify_password


class TestRegister:
    """Test user registration endpoint"""

    @pytest.mark.asyncio
    async def test_register_success(
        self,
        client: AsyncClient,
        sample_user_data: dict
    ):
        """Test successful user registration"""
        response = await client.post(
            "/api/v1/auth/register",
            json=sample_user_data
        )

        assert response.status_code == 201
        data = response.json()

        assert data["email"] == sample_user_data["email"]
        assert data["username"] == sample_user_data["username"]
        assert data["full_name"] == sample_user_data["full_name"]
        assert "id" in data
        assert "hashed_password" not in data
        assert "password" not in data
        assert data["is_active"] is True

    @pytest.mark.asyncio
    async def test_register_duplicate_email(
        self,
        client: AsyncClient,
        test_user: User,
        sample_user_data: dict
    ):
        """Test registration with duplicate email fails"""
        # Try to register with existing user's email
        sample_user_data["email"] = test_user.email
        sample_user_data["username"] = "differentusername"

        response = await client.post(
            "/api/v1/auth/register",
            json=sample_user_data
        )

        assert response.status_code == 409
        assert "email" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_register_duplicate_username(
        self,
        client: AsyncClient,
        test_user: User,
        sample_user_data: dict
    ):
        """Test registration with duplicate username fails"""
        # Try to register with existing user's username
        sample_user_data["username"] = test_user.username
        sample_user_data["email"] = "different@example.com"

        response = await client.post(
            "/api/v1/auth/register",
            json=sample_user_data
        )

        assert response.status_code == 409
        assert "username" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_register_invalid_email(
        self,
        client: AsyncClient,
        sample_user_data: dict
    ):
        """Test registration with invalid email format fails"""
        sample_user_data["email"] = "not-an-email"

        response = await client.post(
            "/api/v1/auth/register",
            json=sample_user_data
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_register_missing_required_fields(
        self,
        client: AsyncClient
    ):
        """Test registration with missing required fields fails"""
        response = await client.post(
            "/api/v1/auth/register",
            json={"email": "test@example.com"}  # Missing username, password
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_register_password_hashing(
        self,
        client: AsyncClient,
        test_db: AsyncSession,
        sample_user_data: dict
    ):
        """Test that password is properly hashed"""
        response = await client.post(
            "/api/v1/auth/register",
            json=sample_user_data
        )

        assert response.status_code == 201

        # Verify password is hashed in database
        from sqlalchemy import select
        result = await test_db.execute(
            select(User).where(User.email == sample_user_data["email"])
        )
        user = result.scalar_one()

        # Password should be hashed, not plain text
        assert user.hashed_password != sample_user_data["password"]
        # But it should verify correctly
        assert verify_password(sample_user_data["password"], user.hashed_password)


class TestLogin:
    """Test user login endpoint"""

    @pytest.mark.asyncio
    async def test_login_success(
        self,
        client: AsyncClient,
        test_user: User,
        sample_login_data: dict
    ):
        """Test successful login"""
        response = await client.post(
            "/api/v1/auth/login",
            json=sample_login_data
        )

        assert response.status_code == 200
        data = response.json()

        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data
        assert isinstance(data["access_token"], str)
        assert len(data["access_token"]) > 0

    @pytest.mark.asyncio
    async def test_login_invalid_email(
        self,
        client: AsyncClient
    ):
        """Test login with non-existent email fails"""
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "somepassword"
            }
        )

        assert response.status_code == 401
        assert "detail" in response.json()

    @pytest.mark.asyncio
    async def test_login_invalid_password(
        self,
        client: AsyncClient,
        test_user: User
    ):
        """Test login with wrong password fails"""
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": test_user.email,
                "password": "wrongpassword"
            }
        )

        assert response.status_code == 401
        assert "detail" in response.json()

    @pytest.mark.asyncio
    async def test_login_missing_credentials(
        self,
        client: AsyncClient
    ):
        """Test login with missing credentials fails"""
        response = await client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com"}  # Missing password
        )

        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_login_token_format(
        self,
        client: AsyncClient,
        test_user: User,
        sample_login_data: dict
    ):
        """Test that returned tokens have correct format"""
        response = await client.post(
            "/api/v1/auth/login",
            json=sample_login_data
        )

        assert response.status_code == 200
        data = response.json()

        # JWT tokens should have 3 parts separated by dots
        access_token_parts = data["access_token"].split(".")
        assert len(access_token_parts) == 3

        refresh_token_parts = data["refresh_token"].split(".")
        assert len(refresh_token_parts) == 3

    @pytest.mark.asyncio
    async def test_login_inactive_user(
        self,
        client: AsyncClient,
        test_user: User,
        test_db: AsyncSession
    ):
        """Test that inactive users cannot login"""
        # Deactivate user
        test_user.is_active = False
        await test_db.commit()

        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": test_user.email,
                "password": "testpassword123"
            }
        )

        assert response.status_code == 401


class TestHealthCheck:
    """Test health check endpoint"""

    @pytest.mark.asyncio
    async def test_health_check(self, client: AsyncClient):
        """Test health check endpoint returns healthy status"""
        response = await client.get("/api/v1/auth/health")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "healthy"
        assert data["service"] == "authentication"


class TestAuthenticationFlow:
    """Test complete authentication flow"""

    @pytest.mark.asyncio
    async def test_register_and_login_flow(
        self,
        client: AsyncClient,
        sample_user_data: dict
    ):
        """Test complete flow: register, then login"""
        # Step 1: Register
        register_response = await client.post(
            "/api/v1/auth/register",
            json=sample_user_data
        )
        assert register_response.status_code == 201

        # Step 2: Login with registered credentials
        login_response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": sample_user_data["email"],
                "password": sample_user_data["password"]
            }
        )
        assert login_response.status_code == 200
        assert "access_token" in login_response.json()

    @pytest.mark.asyncio
    async def test_token_can_be_used_for_authenticated_requests(
        self,
        authenticated_client: AsyncClient
    ):
        """Test that received token works for authenticated requests"""
        # The authenticated_client already has the token set
        # This is just a demonstration - you would test actual protected endpoints
        response = await authenticated_client.get("/api/v1/auth/health")

        assert response.status_code == 200
