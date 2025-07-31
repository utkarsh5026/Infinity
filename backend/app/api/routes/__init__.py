from .auth import router as auth_router
from .topics import router as topics_router
from .user import router as user_router
from .card import router as card_router

__all__ = [
    "auth_router",
    "topics_router",
    "user_router",
    "card_router"
]
