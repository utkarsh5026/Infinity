
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.models import User
from app.schemas.explanation import (
    ExplanationRequest, ExplanationResponse,
    RefinementRequest, RefinementResponse
)
from app.services import ExplanationService
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/explanations", tags=["explanations"])


@router.post("/generate", response_model=ExplanationResponse)
async def generate_explanation(
    request: ExplanationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Generate detailed explanation for a card"""
    explanation_service = ExplanationService(db)

    try:
        explanation = await explanation_service.generate_explanation(
            card_id=request.card_id,
            user_id=current_user.id,
            session_id=request.session_id
        )

        return ExplanationResponse(**explanation)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate explanation")


@router.post("/refine", response_model=RefinementResponse)
async def refine_explanation(
    request: RefinementRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Refine an existing explanation based on user feedback"""
    explanation_service = ExplanationService(db)

    try:
        refined = await explanation_service.refine_explanation(
            explanation_id=request.explanation_id,
            refinement_request=request.refinement_request,
            user_id=current_user.id
        )

        return RefinementResponse(
            **refined,
            refinement_applied=True
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Failed to refine explanation")


@router.get("/stats/{card_id}")
async def get_explanation_stats(
    card_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get explanation statistics for a card (admin only)"""
    # Add admin check here if needed
    explanation_service = ExplanationService(db)

    stats = await explanation_service.get_explanation_stats(card_id)
    return stats
