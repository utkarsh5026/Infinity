from typing import Optional
from loguru import logger
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.config import redis_client, get_db
from .security import verify_token

security = HTTPBearer()


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """
    Get current authenticated user from JWT token.

    This dependency:
    1. Extracts the JWT token from the Authorization header
    2. Verifies the token and gets the user ID
    3. Queries the database for the user
    4. Checks if the user exists and is active
    5. Returns the authenticated user object

    Raises:
        HTTPException: 401 if token is invalid
        HTTPException: 404 if user not found
        HTTPException: 400 if user is inactive
    """
    token = credentials.credentials
    user_id = verify_token(token, token_type="access")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Execute query and get the user object
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    return user


async def get_optional_current_user(
    db: AsyncSession = Depends(get_db),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[User]:
    """
    Get current user if authenticated, otherwise return None.

    This is a non-raising version of get_current_user that returns None
    instead of raising exceptions when authentication fails.
    """
    if not credentials:
        return None

    try:
        token = credentials.credentials
        user_id = verify_token(token, token_type="access")

        if not user_id:
            return None

        result = await db.execute(select(User).where(User.id == int(user_id)))
        user = result.scalar_one_or_none()

        if not user or not user.is_active:
            return None

        return user
    except Exception as e:
        logger.warning(f"Error getting optional user: {e}")
        return None


def get_redis_client():
    """
    Get Redis client dependency
    """
    return redis_client
