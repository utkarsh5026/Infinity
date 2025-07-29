from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.core.security import verify_token
from app.models.user import User
from app.config.redis import redis_client
import logging

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()


def get_current_user(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """
    Get current authenticated user
    """
    token = credentials.credentials
    user_id = verify_token(token, token_type="access")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == user_id).first()
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


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current active user
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current admin user
    """
    if current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


def get_current_educator_or_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current educator or admin user
    """
    if current_user.role.value not in ["educator", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


def get_optional_current_user(
    db: Session = Depends(get_db),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[User]:
    """
    Get current user if authenticated, otherwise None
    """
    if not credentials:
        return None
    
    try:
        token = credentials.credentials
        user_id = verify_token(token, token_type="access")
        
        if not user_id:
            return None
        
        user = db.query(User).filter(User.id == user_id).first()
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


class CommonQueryParams:
    """
    Common query parameters for pagination and filtering
    """
    def __init__(
        self,
        skip: int = 0,
        limit: int = 20,
        sort: Optional[str] = None,
        order: Optional[str] = "asc"
    ):
        self.skip = skip
        self.limit = min(limit, 100)  # Maximum 100 items per page
        self.sort = sort
        self.order = order.lower() if order else "asc"