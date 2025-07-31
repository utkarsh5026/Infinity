from typing import List, Optional
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.config import get_db
from app.models import SavedCard, User
from app.schemas.card import (
    CardResponse,
    SaveCardRequest,
    SavedCardResponse
)
from app.core.dependencies import get_current_user
from app.services.card import CardService
from app.core.exceptions import NotFoundError

router = APIRouter(prefix="/cards", tags=["cards"])


@router.get("/{card_id}")
async def get_card(
    card_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific card by ID"""
    try:
        card = await CardService.get_card_by_id(db, card_id)
        return card
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Error in getting card with the error: {e.message}"
        )


@router.post("/{card_id}/save", response_model=SavedCardResponse)
async def save_card(
    card_id: str,
    request: SaveCardRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Save a card for later review"""
    # Check if already saved
    result = await db.execute(
        select(SavedCard).where(
            and_(
                SavedCard.user_id == current_user.id,
                SavedCard.card_id == card_id
            )
        )
    )
    existing = result.scalar_one_or_none()

    if existing:
        # Update existing
        existing.folder = request.folder or existing.folder
        existing.tags = request.tags or existing.tags
        existing.notes = request.notes or existing.notes
    else:
        # Create new
        saved_card = SavedCard(
            user_id=current_user.id,
            card_id=card_id,
            folder=request.folder,
            tags=request.tags,
            notes=request.notes
        )
        db.add(saved_card)

    await db.commit()

    return saved_card


@router.delete("/{card_id}/save", status_code=status.HTTP_204_NO_CONTENT)
async def unsave_card(
    card_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Remove a card from saved list"""
    try:
        await CardService.delete_card(db, card_id, current_user.id)
        return
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Error in deleting card with the error: {e.message}"
        )


@router.get("/saved", response_model=List[SavedCardResponse])
async def get_saved_cards(
    folder: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's saved cards"""
    query = (
        select(SavedCard)
        .options(selectinload(SavedCard.card))
        .where(SavedCard.user_id == current_user.id)
    )

    if folder:
        query = query.where(SavedCard.folder == folder)

    if tag:
        query = query.where(SavedCard.tags.contains([tag]))

    query = query.order_by(SavedCard.saved_at.desc()).offset(skip).limit(limit)

    result = await db.execute(query)
    saved_cards = result.scalars().all()

    return saved_cards
