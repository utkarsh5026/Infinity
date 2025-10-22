"""
User service for user management and authentication
"""
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, func
from sqlalchemy.exc import IntegrityError
from loguru import logger

from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserPreferencesUpdate,
    PasswordUpdate
)
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token
)
from app.core.exceptions import (
    NotFoundError,
    AuthenticationError,
    DuplicateError,
)


class UserService:
    """Service for user-related operations"""

    def __init__(self, db: AsyncSession):
        self.db = db

    # ========================================================================
    # Internal Helper Methods
    # ========================================================================

    async def _get_user_or_404(self, user_id: int) -> User:
        """
        Get user by ID or raise NotFoundError

        Args:
            user_id: User ID

        Returns:
            User object

        Raises:
            NotFoundError: If user not found
        """
        user = await self.get_user_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return user

    async def _check_email_availability(
        self,
        email: str,
        exclude_user_id: Optional[int] = None
    ) -> None:
        """
        Check if email is available, raise DuplicateError if not

        Args:
            email: Email to check
            exclude_user_id: User ID to exclude from check (for updates)

        Raises:
            DuplicateError: If email is already in use
        """
        existing = await self.get_user_by_email(email)
        if existing and existing.id != exclude_user_id:
            raise DuplicateError("Email already in use")

    async def _check_username_availability(
        self,
        username: str,
        exclude_user_id: Optional[int] = None
    ) -> None:
        """
        Check if username is available, raise DuplicateError if not

        Args:
            username: Username to check
            exclude_user_id: User ID to exclude from check (for updates)

        Raises:
            DuplicateError: If username is already taken
        """
        existing = await self.get_user_by_username(username)
        if existing and existing.id != exclude_user_id:
            raise DuplicateError("Username already taken")

    def _mark_updated(self, user: User) -> None:
        """Mark user as updated with current timestamp"""
        user.updated_at = datetime.now(timezone.utc)

    async def _save_user(self, user: User) -> User:
        """
        Commit and refresh user

        Args:
            user: User object to save

        Returns:
            Refreshed user object
        """
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def _update_user_flag(
        self,
        user_id: int,
        flag_name: str,
        value: bool,
        log_message: str
    ) -> bool:
        """
        Generic method to update user boolean flags

        Args:
            user_id: User ID
            flag_name: Name of the boolean flag to update
            value: New value for the flag
            log_message: Log message to record

        Returns:
            True if successful

        Raises:
            NotFoundError: If user not found
        """
        user = await self._get_user_or_404(user_id)
        setattr(user, flag_name, value)
        self._mark_updated(user)
        await self.db.commit()
        logger.info(f"{log_message}: {user.email} (ID: {user.id})")
        return True

    @staticmethod
    def _get_default_preferences() -> Dict[str, Any]:
        """Get default user preferences for dual-agent system"""
        return {
            "learning_style": "logical",
            "difficulty_level": "intermediate",
            "buddy_personality": "enthusiastic",
            "conversation_pace": "moderate",
            "language": "en",
            "enable_hints": True,
            "enable_animations": True,
            "theme": "light"
        }

    # ========================================================================
    # User Creation and Authentication
    # ========================================================================

    async def create_user(self, user_data: UserCreate) -> User:
        """
        Create a new user account

        Args:
            user_data: User registration data

        Returns:
            Created user object

        Raises:
            DuplicateError: If email or username already exists
        """
        await self._check_email_availability(user_data.email)

        if user_data.username:
            await self._check_username_availability(user_data.username)

        user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=get_password_hash(user_data.password),
            is_active=True,
            is_verified=False,
            is_superuser=False,
            preferences=self._get_default_preferences()
        )

        try:
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            logger.info(f"User created: {user.email} (ID: {user.id})")
            return user
        except IntegrityError as e:
            await self.db.rollback()
            logger.error(f"Database error creating user: {e}")
            raise DuplicateError("User already exists")

    async def authenticate_user(
        self,
        email: str,
        password: str
    ) -> tuple[User, str, str]:
        """
        Authenticate user and generate tokens

        Args:
            email: User email
            password: User password

        Returns:
            Tuple of (user, access_token, refresh_token)

        Raises:
            AuthenticationError: If credentials are invalid
        """
        user = await self.get_user_by_email(email)

        if not user:
            raise AuthenticationError("Invalid email or password")

        if not verify_password(password, user.hashed_password):
            raise AuthenticationError("Invalid email or password")

        if not user.is_active:
            raise AuthenticationError("Account is deactivated")

        user.last_login_at = datetime.now(timezone.utc)
        await self.db.commit()

        access_token = create_access_token(subject=str(user.id))
        refresh_token = create_refresh_token(subject=str(user.id))

        logger.info(f"User authenticated: {user.email} (ID: {user.id})")
        return user, access_token, refresh_token


    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return (await self.db.execute(
            select(User).where(func.lower(User.email) == func.lower(email))
        )).scalar_one_or_none()


    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        result = await self.db.execute(
            select(User).where(func.lower(
                User.username) == func.lower(username))
        )
        return result.scalar_one_or_none()

    async def search_users(
        self,
        query: str,
        limit: int = 20,
        offset: int = 0
    ) -> list[User]:
        """
        Search users by email or username

        Args:
            query: Search query
            limit: Maximum number of results
            offset: Offset for pagination

        Returns:
            List of matching users
        """
        search_pattern = f"%{query}%"
        result = await self.db.execute(
            select(User)
            .where(
                or_(
                    User.email.ilike(search_pattern),
                    User.username.ilike(search_pattern),
                    User.full_name.ilike(search_pattern)
                )
            )
            .where(User.is_active == True)
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    # ========================================================================
    # User Profile Management
    # ========================================================================

    async def update_user_profile(
        self,
        user_id: int,
        updated: UserUpdate
    ) -> User:
        """
        Update user profile

        Args:
            user_id: User ID
            updated: Updated profile data

        Returns:
            Updated user object

        Raises:
            NotFoundError: If user not found
            DuplicateError: If email/username already exists
        """
        user = await self._get_user_or_404(user_id)

        if updated.email and updated.email != user.email:
            await self._check_email_availability(updated.email, user_id)
            user.email = updated.email

        if updated.username and updated.username != user.username:
            await self._check_username_availability(updated.username, user_id)
            user.username = updated.username

        if updated.full_name is not None:
            user.full_name = updated.full_name

        if updated.avatar_url is not None:
            user.avatar_url = updated.avatar_url

        self._mark_updated(user)

        try:
            await self._save_user(user)
            logger.info(f"User profile updated: {user.email} (ID: {user.id})")
            return user
        except IntegrityError:
            await self.db.rollback()
            raise DuplicateError("Profile update failed")

    async def update_password(
        self,
        user_id: int,
        password_data: PasswordUpdate
    ) -> bool:
        """
        Update user password

        Args:
            user_id: User ID
            password_data: Current and new password

        Returns:
            True if successful

        Raises:
            NotFoundError: If user not found
            AuthenticationError: If current password is incorrect
        """
        user = await self._get_user_or_404(user_id)

        if not verify_password(password_data.current_password, user.hashed_password):
            raise AuthenticationError("Current password is incorrect")

        user.hashed_password = get_password_hash(password_data.new_password)
        self._mark_updated(user)

        await self.db.commit()
        logger.info(f"Password updated for user: {user.email} (ID: {user.id})")
        return True

    async def update_preferences(
        self,
        user_id: int,
        pref: UserPreferencesUpdate
    ) -> Dict[str, Any]:
        """
        Update user preferences for dual-agent system

        Args:
            user_id: User ID
            pref: Updated preferences

        Returns:
            Updated preferences dictionary

        Raises:
            NotFoundError: If user not found
        """
        user = await self._get_user_or_404(user_id)

        current_prefs = user.preferences or {}

        update_dict = pref.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            if value is not None:
                current_prefs[key] = value

        user.preferences = current_prefs
        self._mark_updated(user)

        await self._save_user(user)

        logger.info(
            f"Preferences updated for user: {user.email} (ID: {user.id})")
        return user.preferences

    async def get_preferences(self, user_id: int) -> Dict[str, Any]:
        """
        Get user preferences

        Args:
            user_id: User ID

        Returns:
            User preferences dictionary

        Raises:
            NotFoundError: If user not found
        """
        user = await self._get_user_or_404(user_id)
        return user.preferences or self._get_default_preferences()

    async def deactivate_user(self, user_id: int) -> bool:
        """
        Deactivate user account

        Args:
            user_id: User ID

        Returns:
            True if successful

        Raises:
            NotFoundError: If user not found
        """
        user = await self.get_user_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

        user.is_active = False
        user.updated_at = datetime.now(timezone.utc)

        await self.db.commit()
        logger.info(f"User deactivated: {user.email} (ID: {user.id})")
        return True

    async def activate_user(self, user_id: int) -> bool:
        """
        Activate user account

        Args:
            user_id: User ID

        Returns:
            True if successful

        Raises:
            NotFoundError: If user not found
        """
        user = await self.get_user_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

        user.is_active = True
        user.updated_at = datetime.now(timezone.utc)

        await self.db.commit()
        logger.info(f"User activated: {user.email} (ID: {user.id})")
        return True

    async def verify_user_email(self, user_id: int) -> bool:
        """
        Mark user email as verified

        Args:
            user_id: User ID

        Returns:
            True if successful

        Raises:
            NotFoundError: If user not found
        """
        user = await self.get_user_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

        user.is_verified = True
        user.updated_at = datetime.now(timezone.utc)

        await self.db.commit()
        logger.info(f"User email verified: {user.email} (ID: {user.id})")
        return True


