from fastapi import APIRouter, HTTPException
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from pydantic import BaseModel
from app.core.config import settings
from typing import Optional

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    temperature: Optional[float] = 0.7


class ChatResponse(BaseModel):
    response: str
    model: str


@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """Chat with AI using LangChain and OpenAI"""
    if not settings.OPENAI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="OpenAI API key not configured. Please set OPENAI_API_KEY in environment variables."
        )

    try:
        # Initialize ChatOpenAI
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=request.temperature,
            openai_api_key=settings.OPENAI_API_KEY
        )

        # Create message
        message = HumanMessage(content=request.message)

        # Get response
        response = llm.invoke([message])

        return ChatResponse(
            response=response.content,
            model="gpt-3.5-turbo"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing request: {str(e)}")


@router.get("/models")
async def get_available_models():
    """Get list of available AI models"""
    return {
        "models": [
            {"name": "gpt-3.5-turbo", "description": "Fast and efficient for most tasks"},
            {"name": "gpt-4", "description": "More capable but slower"},
        ]
    }


@router.post("/summarize")
async def summarize_text(text: str):
    """Summarize given text using AI"""
    if not settings.OPENAI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="OpenAI API key not configured"
        )

    try:
        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.3,
            openai_api_key=settings.OPENAI_API_KEY
        )

        prompt = f"Please provide a concise summary of the following text:\n\n{text}"
        message = HumanMessage(content=prompt)
        response = llm.invoke([message])

        return {"summary": response.content}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error summarizing text: {str(e)}")
