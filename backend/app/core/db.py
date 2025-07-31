from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Any, Dict
from enum import Enum


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class IsolationLevel(str, Enum):
    READ_UNCOMMITTED = "READ_UNCOMMITTED"
    READ_COMMITTED = "READ_COMMITTED"
    REPEATABLE_READ = "REPEATABLE_READ"
    SERIALIZABLE = "SERIALIZABLE"


class DBOperationOptions(BaseModel):
    """Options for database operations"""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    commit: bool = True
    refresh: bool = True
    close: bool = False
    isolation_level: Optional[IsolationLevel] = None

    limit: Optional[int] = Field(default=None, ge=1, le=100)
    skip: Optional[int] = Field(default=0, ge=0)

    # Sorting
    sort_by: Optional[str] = None
    sort_order: SortOrder = SortOrder.ASC

    # Filtering
    filters: Optional[Dict[str, Any]] = None

    # Performance options
    lazy_load: bool = True
    eager_load_relations: Optional[list[str]] = None

    # Bulk operations
    batch_size: Optional[int] = Field(default=None, ge=1, le=1000)

    # Query options
    include_soft_deleted: bool = False
    lock_rows: bool = False


class PaginationMeta(BaseModel):
    """Pagination metadata for responses"""
    total: int
    page: int
    per_page: int
    pages: int
    has_next: bool
    has_prev: bool


class PaginatedResponse(BaseModel):
    """Generic paginated response"""
    items: list[Any]
    meta: PaginationMeta


class DBResult(BaseModel):
    """Result of a database operation"""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    affected_rows: Optional[int] = None


# Utility functions
def create_pagination_meta(
    total: int,
    skip: int,
    limit: int
) -> PaginationMeta:
    """Create pagination metadata"""
    page = (skip // limit) + 1 if limit else 1
    pages = (total + limit - 1) // limit if limit else 1

    return PaginationMeta(
        total=total,
        page=page,
        per_page=limit or total,
        pages=pages,
        has_next=page < pages,
        has_prev=page > 1
    )
