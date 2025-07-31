from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.topics import TopicService
from app.config.database import get_db
from app.schemas.topic import TopicResponse, TopicListResponse
from backend.app.core.db import DBOperationOptions

router = APIRouter(prefix="/topics", tags=["topics"])


@router.get("/", response_model=TopicListResponse)
async def get_topics(
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
) -> TopicListResponse:
    """Get list of available topics"""

    topics, total = await TopicService.get_topics(
        db, category, search, options=DBOperationOptions(
            skip=skip,
            limit=limit
        )
    )

    return TopicListResponse(
        topics=topics,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/trending", response_model=list[TopicResponse])
async def get_trending_topics(
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
) -> list[TopicResponse]:
    """Get trending topics based on recent activity"""
    return await TopicService.get_trending_topics(db, limit)
