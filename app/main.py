from fastapi import FastAPI
from app.core.middleware import setup_middleware
from app.core.events import setup_events
from app.config.settings import settings
from app.api.v1.router import api_router
from app.config.database import engine
from app.models import Base

# Create database tables
Base.metadata.create_all(bind=engine)


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="Advanced Learning Platform Backend with AI Integration",
        version="1.0.0",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        debug=settings.DEBUG
    )

    # Setup middleware
    setup_middleware(app)

    # Setup event handlers
    setup_events(app)

    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app


app = create_application()


@app.get("/")
async def root():
    return {
        "message": "Welcome to Infinity Learning Platform",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "infinity-backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
