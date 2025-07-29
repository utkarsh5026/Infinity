from fastapi import APIRouter
from app.api.routes import users, items, langchain_routes

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(langchain_routes.router, prefix="/ai", tags=["ai"])
