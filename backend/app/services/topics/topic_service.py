from typing import Optional
from datetime import timedelta
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Topic, LearningSession
from app.core.db import DBOperationOptions


class TopicService:
    """Service for managing topic operations"""

    async def get_topics(
        self,
        db: AsyncSession,
        category: Optional[str],
        search: Optional[str],
        options: DBOperationOptions,
    ):
        """Get list of available topics"""
        query = select(Topic)

        if category:
            query = query.where(Topic.category == category)

        if search:
            query = query.where(Topic.name.ilike(f"%{search}%"))

        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()

        skip, limit = options.skip, options.limit

        query = query.order_by(
            Topic.popularity_score.desc()
        ).offset(skip).limit(limit)
        result = await db.execute(query)
        topics = result.scalars().all()

        return topics, total

    async def get_trending_topics(
        self,
        db: AsyncSession,
        limit: int,
    ):
        """Get trending topics based on recent activity"""
        subquery = (
            select(
                LearningSession.topic_id,
                func.count(LearningSession.id).label("session_count")
            )
            .where(LearningSession.started_at >= func.now() - timedelta(days=7))
            .group_by(LearningSession.topic_id)
            .subquery()
        )

        query = (
            select(Topic)
            .join(subquery, Topic.id == subquery.c.topic_id)
            .order_by(subquery.c.session_count.desc())
            .limit(limit)
        )

        result = await db.execute(query)
        topics = result.scalars().all()
        return topics
