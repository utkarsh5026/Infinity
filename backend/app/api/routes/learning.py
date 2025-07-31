from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_, func
from sqlalchemy.orm import selectinload

from app.config.database import get_db
from app.models import User, Topic, Card, LearningSession, CardInteraction
from app.schemas.learning import (
    StartSessionRequest, StartSessionResponse,
    CardResponse, SessionMetricsUpdate,
    SessionStatsResponse
)
from app.services.learning import LearningService
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/learning", tags=["learning"])


@router.post("/start", response_model=StartSessionResponse)
async def start_learning_session(
    request: StartSessionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Start a new learning session"""
    learning_service = LearningService(db)

    result = await db.execute(
        select(Topic).where(Topic.name == request.topic)
    )
    topic = result.scalar_one_or_none()

    if not topic:
        topic = Topic(
            name=request.topic,
            slug=request.topic.lower().replace(" ", "-"),
            category=request.category or "general"
        )
        db.add(topic)
        await db.commit()
        await db.refresh(topic)

    session_data = await learning_service.initialize_session(
        topic_id=topic.id,
        user_id=current_user.id,
        mode=request.mode
    )

    return session_data


@router.get("/session/{session_id}/next", response_model=CardResponse)
async def get_next_card(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get next card in the learning session"""
    # Verify session belongs to user
    result = await db.execute(
        select(LearningSession).where(
            and_(
                LearningSession.id == session_id,
                LearningSession.user_id == current_user.id
            )
        )
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    learning_service = LearningService(db)
    card = await learning_service.get_next_card(session_id)

    if not card:
        raise HTTPException(status_code=404, detail="No more cards available")

    return card


@router.post("/session/{session_id}/metrics")
async def update_card_metrics(
    session_id: str,
    metrics: SessionMetricsUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update metrics for a viewed card"""
    # Create interaction record
    interaction = CardInteraction(
        user_id=current_user.id,
        card_id=metrics.card_id,
        session_id=session_id,
        time_spent_seconds=metrics.time_spent,
        answer_revealed=metrics.answer_revealed,
        action=metrics.action,
        confidence_rating=metrics.confidence_rating
    )
    db.add(interaction)

    # Update card statistics
    await db.execute(
        update(Card)
        .where(Card.id == metrics.card_id)
        .values(
            total_views=Card.total_views + 1,
            total_time_spent=Card.total_time_spent + metrics.time_spent
        )
    )

    # Update session metrics
    await db.execute(
        update(LearningSession)
        .where(LearningSession.id == session_id)
        .values(
            cards_viewed=LearningSession.cards_viewed + 1,
            total_time_seconds=LearningSession.total_time_seconds + metrics.time_spent
        )
    )

    await db.commit()

    return {"status": "updated"}


@router.get("/session/{session_id}/stats", response_model=SessionStatsResponse)
async def get_session_stats(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get detailed statistics for a learning session"""
    result = await db.execute(
        select(LearningSession)
        .options(selectinload(LearningSession.card_interactions))
        .where(
            and_(
                LearningSession.id == session_id,
                LearningSession.user_id == current_user.id
            )
        )
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Calculate stats
    total_cards = len(session.card_interactions)
    cards_mastered = sum(
        1 for i in session.card_interactions if i.confidence_rating >= 4)
    avg_time = sum(
        i.time_spent_seconds for i in session.card_interactions) / max(total_cards, 1)

    return SessionStatsResponse(
        session_id=session_id,
        cards_viewed=session.cards_viewed,
        cards_mastered=cards_mastered,
        total_time_seconds=session.total_time_seconds,
        average_time_per_card=avg_time,
        completion_rate=(cards_mastered / max(total_cards, 1)) * 100,
        engagement_score=session.engagement_score
    )


@router.post("/session/{session_id}/end")
async def end_learning_session(
    session_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """End a learning session"""
    await db.execute(
        update(LearningSession)
        .where(
            and_(
                LearningSession.id == session_id,
                LearningSession.user_id == current_user.id
            )
        )
        .values(ended_at=datetime.utcnow())
    )
    await db.commit()

    return {"status": "session ended"}
