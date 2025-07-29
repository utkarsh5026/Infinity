# Infinity Learning Platform - Backend

A comprehensive learning platform backend built with FastAPI, featuring AI-powered content generation, advanced analytics, and scalable architecture.

## 🏗️ Architecture Overview

This backend follows a modern, scalable architecture with clear separation of concerns:

- **Configuration Layer**: Environment-based settings and database management
- **Core Layer**: Security, middleware, exceptions, and common utilities  
- **Models Layer**: SQLAlchemy models with comprehensive relationships
- **Services Layer**: Business logic with AI/LLM and vector database integrations
- **API Layer**: RESTful endpoints with comprehensive validation
- **CRUD Layer**: Database operations with caching strategies

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py                     # FastAPI application entry point
│   ├── config/                     # Configuration management
│   │   ├── settings.py             # Environment-specific configurations
│   │   ├── database.py             # Database connection and session management
│   │   ├── redis.py                # Redis connection configuration
│   │   └── logging.py              # Logging configuration
│   ├── core/                       # Core application modules
│   │   ├── security.py             # JWT, password hashing, auth utilities
│   │   ├── dependencies.py         # FastAPI dependency injection
│   │   ├── exceptions.py           # Custom exception classes
│   │   ├── middleware.py           # Custom middleware (CORS, logging, etc.)
│   │   └── events.py               # Startup/shutdown event handlers
│   ├── models/                     # SQLAlchemy models
│   │   ├── base.py                 # Base model with common fields
│   │   ├── user.py                 # User model with preferences
│   │   ├── topic.py                # Learning topics and categories
│   │   ├── content.py              # Learning cards and content
│   │   ├── session.py              # Learning sessions and progress
│   │   ├── analytics.py            # User interaction analytics
│   │   └── associations.py         # Many-to-many relationship tables
│   ├── schemas/                    # Pydantic schemas
│   │   ├── base.py                 # Base Pydantic schemas
│   │   ├── user.py                 # User request/response schemas
│   │   ├── topic.py                # Topic schemas
│   │   ├── content.py              # Content schemas
│   │   ├── session.py              # Session schemas
│   │   └── analytics.py            # Analytics schemas
│   ├── api/                        # API endpoints
│   │   ├── deps.py                 # API dependencies
│   │   └── v1/
│   │       ├── router.py           # Main API router
│   │       └── endpoints/
│   │           ├── auth.py         # Authentication endpoints
│   │           ├── users.py        # User management
│   │           ├── topics.py       # Topic management
│   │           ├── content.py      # Content CRUD operations
│   │           ├── learning.py     # Learning session endpoints
│   │           ├── analytics.py    # Analytics and progress tracking
│   │           └── admin.py        # Admin-only endpoints
│   ├── services/                   # Business logic services
│   │   ├── auth_service.py         # Authentication business logic
│   │   ├── user_service.py         # User management service
│   │   ├── content_service.py      # Content management service
│   │   ├── learning_service.py     # Learning session management
│   │   ├── analytics_service.py    # Analytics computation
│   │   ├── llm/                    # AI/LLM integration
│   │   │   ├── base.py             # Abstract LLM interface
│   │   │   ├── openai_client.py    # OpenAI GPT integration
│   │   │   ├── anthropic_client.py # Claude integration
│   │   │   ├── content_generator.py # Content generation orchestrator
│   │   │   ├── prompt_templates.py # LLM prompt templates
│   │   │   └── content_validator.py # Generated content validation
│   │   ├── vector/                 # Vector database integration
│   │   │   ├── base.py             # Abstract vector database interface
│   │   │   ├── pinecone_client.py  # Pinecone integration
│   │   │   ├── chroma_client.py    # Chroma integration
│   │   │   └── semantic_search.py  # Semantic content search
│   │   ├── cache/                  # Caching services
│   │   │   ├── redis_client.py     # Redis caching service
│   │   │   └── cache_strategies.py # Caching strategies and TTL management
│   │   └── external/               # External service integrations
│   │       ├── s3_client.py        # AWS S3 media storage
│   │       ├── cloudinary_client.py # Cloudinary integration
│   │       └── moderation_client.py # Content moderation service
│   ├── tasks/                      # Background tasks (Celery)
│   │   ├── celery_app.py           # Celery configuration
│   │   ├── content_generation.py   # Background content generation
│   │   ├── analytics_processing.py # Analytics computation tasks
│   │   └── notifications.py        # Push notification tasks
│   ├── crud/                       # Database operations
│   │   ├── base.py                 # Base CRUD operations
│   │   ├── user.py                 # User CRUD operations
│   │   ├── topic.py                # Topic CRUD operations
│   │   ├── content.py              # Content CRUD operations
│   │   └── session.py              # Session CRUD operations
│   ├── utils/                      # Utility functions
│   │   ├── validators.py           # Custom validation functions
│   │   ├── formatters.py           # Data formatting utilities
│   │   ├── constants.py            # Application constants
│   │   └── helpers.py              # General utility functions
│   └── tests/                      # Test suite
│       ├── conftest.py             # Pytest configuration and fixtures
│       ├── test_auth.py            # Authentication tests
│       ├── test_content.py         # Content generation tests
│       ├── test_learning.py        # Learning flow tests
│       └── test_analytics.py       # Analytics tests
├── migrations/                     # Alembic database migrations
├── scripts/                        # Utility scripts
├── docker/                         # Docker configuration
├── requirements/                   # Python dependencies
├── .env.example                    # Environment variables template
├── pyproject.toml                  # Python project configuration
└── README.md
```

## 🚀 Features

### Core Features
- **User Management**: Complete user authentication, authorization, and profile management
- **Learning Content**: Flexible content system supporting various types (cards, videos, articles, quizzes)
- **Learning Sessions**: Track user progress and learning sessions with detailed analytics
- **Spaced Repetition**: Built-in spaced repetition system for optimal learning
- **Analytics**: Comprehensive user analytics and learning progress tracking

### AI/ML Features  
- **Content Generation**: AI-powered learning content generation using OpenAI/Anthropic
- **Semantic Search**: Vector database integration for intelligent content discovery
- **Content Moderation**: Automated content filtering and safety checks
- **Personalization**: AI-driven learning path recommendations

### Technical Features
- **Async/Await**: Full async support for high performance
- **Caching**: Redis integration for high-performance caching
- **Background Tasks**: Celery integration for async task processing
- **Security**: JWT authentication, rate limiting, security headers
- **Monitoring**: Comprehensive logging and request tracking
- **Scalability**: Microservices-ready architecture

## 🛠️ Setup

### Prerequisites
- Python 3.12+
- Poetry
- Redis (optional, for caching)
- PostgreSQL (optional, SQLite works for development)

### Installation

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   poetry install
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

4. **Run the application:**
   ```bash
   poetry run python app/main.py
   ```

### API Documentation
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## 🔧 Development

### Database Migrations
```bash
# Initialize Alembic (if not done)
poetry run alembic init migrations

# Create migration
poetry run alembic revision --autogenerate -m "Description"

# Apply migration
poetry run alembic upgrade head
```

### Code Quality
```bash
# Format code
poetry run black .

# Sort imports
poetry run isort .

# Type checking
poetry run mypy .
```

### Testing
```bash
# Run tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=app
```

## 🏭 Production Deployment

### Environment Variables
See `.env.example` for all required environment variables.

### Docker Deployment
```bash
# Build image
docker build -f docker/Dockerfile -t infinity-backend .

# Run with docker-compose
docker-compose -f docker/docker-compose.prod.yml up -d
```

### Manual Deployment
```bash
# Install production dependencies
poetry install --no-dev

# Run with Gunicorn
poetry run gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 📊 API Overview

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/refresh` - Refresh token
- `POST /api/v1/auth/logout` - User logout

### Users
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update profile
- `GET /api/v1/users/{id}` - Get user by ID

### Topics
- `GET /api/v1/topics/` - List topics
- `POST /api/v1/topics/` - Create topic
- `GET /api/v1/topics/{id}` - Get topic details

### Content
- `GET /api/v1/content/` - List content
- `POST /api/v1/content/` - Create content
- `POST /api/v1/content/generate` - AI-generate content

### Learning
- `POST /api/v1/learning/sessions` - Start learning session
- `PUT /api/v1/learning/sessions/{id}` - Update session progress
- `GET /api/v1/learning/progress` - Get learning progress

### Analytics
- `GET /api/v1/analytics/dashboard` - User dashboard data
- `GET /api/v1/analytics/progress` - Learning progress analytics
- `GET /api/v1/analytics/reports` - Detailed reports

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.
