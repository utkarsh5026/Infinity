from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import api_router


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="FastAPI backend with SQLAlchemy and LangChain",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI backend with SQLAlchemy and LangChain"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
