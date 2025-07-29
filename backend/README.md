# FastAPI Backend with SQLAlchemy and LangChain

A modern Python web application built with FastAPI, SQLAlchemy, and LangChain integration.

## Features

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM)
- **LangChain**: Framework for developing applications with language models
- **Poetry**: Dependency management and packaging
- **Async Support**: Full async/await support for better performance
- **API Documentation**: Automatic interactive API docs with Swagger UI

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── users.py          # User CRUD operations
│   │   │   ├── items.py          # Item CRUD operations
│   │   │   └── langchain_routes.py  # AI/LangChain endpoints
│   │   └── api.py               # Main API router
│   ├── core/
│   │   └── config.py            # App configuration
│   ├── db/
│   │   └── database.py          # Database setup
│   └── schemas/
│       ├── user.py              # User Pydantic models
│       └── item.py              # Item Pydantic models
├── models/
│   ├── user.py                  # User SQLAlchemy model
│   └── item.py                  # Item SQLAlchemy model
├── main.py                      # FastAPI app entry point
├── pyproject.toml               # Poetry configuration
└── env_template.txt             # Environment variables template
```

## Setup

### Prerequisites

- Python 3.12+
- Poetry (for dependency management)

### Installation

1. **Clone and navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Install dependencies**:
   ```bash
   poetry install
   ```

3. **Set up environment variables**:
   ```bash
   # Copy the template and edit with your values
   cp env_template.txt .env
   ```
   
   Edit `.env` file with your actual values:
   ```
   DATABASE_URL=sqlite:///./app.db
   OPENAI_API_KEY=your_actual_openai_api_key
   ```

4. **Activate the virtual environment**:
   ```bash
   poetry shell
   ```

## Running the Application

### Development Server

```bash
# From the backend directory
poetry run python main.py
```

or

```bash
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at:
- **API**: http://localhost:8000
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## API Endpoints

### Core Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check

### Users (`/api/v1/users`)

- `GET /api/v1/users/` - Get all users
- `GET /api/v1/users/{user_id}` - Get user by ID
- `POST /api/v1/users/` - Create new user

### Items (`/api/v1/items`)

- `GET /api/v1/items/` - Get all items
- `GET /api/v1/items/{item_id}` - Get item by ID
- `POST /api/v1/items/` - Create new item
- `DELETE /api/v1/items/{item_id}` - Delete item

### AI/LangChain (`/api/v1/ai`)

- `POST /api/v1/ai/chat` - Chat with AI
- `GET /api/v1/ai/models` - Get available models
- `POST /api/v1/ai/summarize` - Summarize text

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///./app.db` |
| `OPENAI_API_KEY` | OpenAI API key for LangChain | Required for AI features |
| `PROJECT_NAME` | Application name | `"Infinity Backend"` |
| `API_V1_STR` | API version prefix | `"/api/v1"` |

## Development

### Code Formatting

```bash
# Format code with Black
poetry run black .

# Sort imports with isort
poetry run isort .

# Type checking with mypy
poetry run mypy .
```

### Testing

```bash
# Run tests with pytest
poetry run pytest

# Run async tests
poetry run pytest -v
```

## Database

The application uses SQLite by default. The database file (`app.db`) will be created automatically when you first run the application.

### Models

- **User**: username, email, hashed_password, is_active, timestamps
- **Item**: title, description, owner_id, is_active, timestamps

## LangChain Integration

The application includes LangChain integration for AI features:

1. **Chat endpoint**: Interactive chat with OpenAI models
2. **Text summarization**: Summarize large text blocks
3. **Model selection**: Choose from different AI models

**Note**: You need to set your `OPENAI_API_KEY` in the `.env` file to use AI features.

## CORS Configuration

The application is configured to allow CORS requests from:
- `http://localhost:3000` (React frontend)
- Other origins can be configured in the settings

## Production Deployment

For production deployment:

1. Set production environment variables
2. Use a production database (PostgreSQL recommended)
3. Set up proper logging
4. Use a production ASGI server like Gunicorn with Uvicorn workers

```bash
poetry run gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```