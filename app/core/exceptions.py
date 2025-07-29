from typing import Any, Dict, Optional


class InfinityException(Exception):
    """
    Base exception class for Infinity application
    """

    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(message)


class ValidationError(InfinityException):
    """
    Raised when data validation fails
    """
    pass


class AuthenticationError(InfinityException):
    """
    Raised when authentication fails
    """
    pass


class AuthorizationError(InfinityException):
    """
    Raised when user doesn't have required permissions
    """
    pass


class NotFoundError(InfinityException):
    """
    Raised when a resource is not found
    """
    pass


class DuplicateError(InfinityException):
    """
    Raised when trying to create a duplicate resource
    """
    pass


class BusinessLogicError(InfinityException):
    """
    Raised when business logic validation fails
    """
    pass


class ExternalServiceError(InfinityException):
    """
    Raised when external service call fails
    """
    pass


class RateLimitError(InfinityException):
    """
    Raised when rate limit is exceeded
    """
    pass


class DatabaseError(InfinityException):
    """
    Raised when database operation fails
    """
    pass


class LLMError(InfinityException):
    """
    Raised when LLM service fails
    """
    pass


class VectorDatabaseError(InfinityException):
    """
    Raised when vector database operation fails
    """
    pass


class ContentGenerationError(InfinityException):
    """
    Raised when content generation fails
    """
    pass


class FileUploadError(InfinityException):
    """
    Raised when file upload fails
    """
    pass


class CacheError(InfinityException):
    """
    Raised when cache operation fails
    """
    pass
