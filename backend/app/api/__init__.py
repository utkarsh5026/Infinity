from fastapi import APIRouter
from app.api.routes import (
    auth_router,
    topics_router,
    user_router,
    card_router,
    explanation_router
)

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(topics_router)
api_router.include_router(user_router)
api_router.include_router(card_router)
api_router.include_router(explanation_router)
