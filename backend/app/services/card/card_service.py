from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_

from app.models import Card, SavedCard
from app.core.exceptions import NotFoundError
from app.schemas.card import SaveCardRequest


class CardService:
    """Service for managing card operations"""

    async def get_card_by_id(
        self,
        db: AsyncSession,
        card_id: str
    ):
        """Get a card by ID"""
        result = await db.execute(
            select(Card).where(Card.id == card_id)
        )
        card = result.scalar_one_or_none()
        if not card:
            raise NotFoundError(
                f"Card with ID {card_id} not found"
            )
        return card

    async def delete_card(
        self,
        db: AsyncSession,
        card_id: str,
        user_id: str
    ):
        """Delete a card from saved list"""
        result = await db.execute(
            select(SavedCard).where(
                and_(
                    SavedCard.user_id == user_id,
                    SavedCard.card_id == card_id
                )
            )
        )
        saved_card = result.scalar_one_or_none()

        if not saved_card:
            raise NotFoundError(
                f"Card with ID {card_id} not found in saved list"
            )

        await db.delete(saved_card)
        await db.commit()

    async def save_or_update_card(
        self,
        db: AsyncSession,
        card_id: str,
        user_id: str,
        update_data: SaveCardRequest
    ) -> tuple[SavedCard, bool]:
        """Save or update a card in saved list"""
        result = await db.execute(
            select(SavedCard).where(
                and_(
                    SavedCard.user_id == user_id,
                    SavedCard.card_id == card_id
                )
            )
        )
        existing = result.scalar_one_or_none()
        folder, tags, notes = update_data.folder, update_data.tags, update_data.notes

        if existing:
            existing.folder = folder or existing.folder
            existing.tags = tags or existing.tags
            existing.notes = notes or existing.notes
            await db.commit()
            await db.refresh(existing)
            return existing, False

        saved_card = SavedCard(
            user_id=user_id,
            card_id=card_id,
            folder=folder,
            tags=tags,
            notes=notes
        )
        db.add(saved_card)
        await db.commit()
        return saved_card, True
