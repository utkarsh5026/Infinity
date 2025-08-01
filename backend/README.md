# Infinity Learning Platform - API Documentation

## Base Information

**Base URL:** `http://localhost:8000/api/v1` (Development)  
**Content-Type:** `application/json`  
**Authentication:** Bearer Token (JWT)

## Authentication Flow

### Overview
The API uses JWT (JSON Web Tokens) for authentication. After login, you'll receive an access token that must be included in the `Authorization` header for protected routes.

**Header Format:**
```
Authorization: Bearer <your_access_token>
```

---

## 🔐 Authentication Endpoints

### 1. Register New User
**Endpoint:** `POST /auth/register`  
**Authentication:** None required

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepassword123",
  "full_name": "John Doe" // Optional
}
```

**Validation Rules:**
- `username`: Must be alphanumeric, minimum 3 characters
- `password`: Minimum 8 characters
- `email`: Valid email format

**Success Response (201):**
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "avatar_url": null,
  "preferred_difficulty": 3,
  "learning_style": "mixed",
  "daily_goal": 20,
  "is_premium": false
}
```

**Error Response (400):**
```json
{
  "detail": "Email or username already registered"
}
```

### 2. Login (Get Access Token)
**Endpoint:** `POST /auth/token`  
**Authentication:** None required  
**Content-Type:** `application/x-www-form-urlencoded`

**Request Body (Form Data):**
```
username=johndoe (or email)
password=securepassword123
```

**Success Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Response (401):**
```json
{
  "detail": "Incorrect username or password"
}
```

---

## 👤 User Management Endpoints

### 3. Get Current User Profile
**Endpoint:** `GET /users/me`  
**Authentication:** Required

**Success Response (200):**
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "username": "johndoe",
  "full_name": "John Doe",
  "avatar_url": "https://example.com/avatar.jpg",
  "preferred_difficulty": 3,
  "learning_style": "mixed",
  "daily_goal": 20,
  "is_premium": false
}
```

### 4. Update User Profile
**Endpoint:** `PATCH /users/me`  
**Authentication:** Required

**Request Body (all fields optional):**
```json
{
  "full_name": "John Updated Doe",
  "avatar_url": "https://example.com/new-avatar.jpg",
  "bio": "Software developer and lifelong learner"
}
```

**Success Response (200):** Same as Get Profile

### 5. Update User Learning Preferences
**Endpoint:** `PATCH /users/me/preferences`  
**Authentication:** Required

**Request Body (all fields optional):**
```json
{
  "preferred_difficulty": 4,
  "learning_style": "visual",
  "daily_goal": 30,
  "notification_enabled": true
}
```

**Field Constraints:**
- `preferred_difficulty`: Integer 1-5
- `learning_style`: One of "visual", "textual", "practical", "mixed"
- `daily_goal`: Integer 1-100

**Success Response (200):** Updated user profile

---

## 📚 Topics Endpoints

### 6. Get Topics List
**Endpoint:** `GET /topics/`  
**Authentication:** Optional

**Query Parameters:**
- `category` (optional): Filter by category (string)
- `search` (optional): Search term (string)
- `skip` (optional): Number of records to skip (integer, default: 0)
- `limit` (optional): Maximum records to return (integer, default: 20, max: 100)

**Example Request:**
```
GET /topics/?category=programming&search=python&skip=0&limit=10
```

**Success Response (200):**
```json
{
  "topics": [
    {
      "id": "uuid-string",
      "name": "Python Programming",
      "slug": "python-programming",
      "category": "programming",
      "description": "Learn Python from basics to advanced",
      "icon_url": "https://example.com/python-icon.png",
      "cover_image_url": "https://example.com/python-cover.jpg",
      "difficulty_range": {
        "min": 1,
        "max": 5
      },
      "estimated_cards": 120,
      "popularity_score": 8.5
    }
  ],
  "total": 1,
  "skip": 0,
  "limit": 10
}
```

### 7. Get Trending Topics
**Endpoint:** `GET /topics/trending`  
**Authentication:** Optional

**Query Parameters:**
- `limit` (optional): Maximum topics to return (integer, default: 10, max: 50)

**Success Response (200):**
```json
[
  {
    "id": "uuid-string",
    "name": "Machine Learning",
    "slug": "machine-learning",
    "category": "ai",
    "description": "Introduction to ML concepts",
    "icon_url": "https://example.com/ml-icon.png",
    "cover_image_url": "https://example.com/ml-cover.jpg",
    "difficulty_range": {
      "min": 2,
      "max": 5
    },
    "estimated_cards": 85,
    "popularity_score": 9.2
  }
]
```

---

## 🎯 Learning Session Endpoints

### 8. Start Learning Session
**Endpoint:** `POST /learning/start`  
**Authentication:** Required

**Request Body:**
```json
{
  "topic": "Python Programming",
  "category": "programming", // Optional, default: "general"
  "mode": "standard" // Options: "standard", "rapid_fire", "deep_dive", "practice"
}
```

**Success Response (200):**
```json
{
  "session_id": "uuid-string",
  "initial_cards": [
    {
      "id": "card-uuid",
      "question": "What is a variable in Python?",
      "answer": "A **variable** is a container for storing data values",
      "difficulty": 1,
      "concept_tag": "Python Basics"
    }
  ],
  "total_concepts": 7
}
```

### 9. Get Next Card in Session
**Endpoint:** `GET /learning/session/{session_id}/next`  
**Authentication:** Required

**Success Response (200):**
```json
{
  "id": "card-uuid",
  "question": "How do you create a list in Python?",
  "answer": "Use square brackets: `my_list = [1, 2, 3]`",
  "difficulty": 2,
  "concept_tag": "Python Data Structures"
}
```

**Error Response (404):**
```json
{
  "detail": "No more cards available"
}
```

### 10. Update Card Interaction Metrics
**Endpoint:** `POST /learning/session/{session_id}/metrics`  
**Authentication:** Required

**Request Body:**
```json
{
  "card_id": "card-uuid",
  "time_spent": 15.5,
  "answer_revealed": true,
  "action": "view", // Options: "view", "skip", "save", "master"
  "confidence_rating": 4 // Optional, 1-5 scale
}
```

**Success Response (200):**
```json
{
  "status": "updated"
}
```

### 11. Get Session Statistics
**Endpoint:** `GET /learning/session/{session_id}/stats`  
**Authentication:** Required

**Success Response (200):**
```json
{
  "session_id": "uuid-string",
  "cards_viewed": 15,
  "cards_mastered": 8,
  "total_time_seconds": 450.5,
  "average_time_per_card": 30.03,
  "completion_rate": 53.33,
  "engagement_score": 7.8
}
```

### 12. End Learning Session
**Endpoint:** `POST /learning/session/{session_id}/end`  
**Authentication:** Required

**Success Response (200):**
```json
{
  "status": "session ended"
}
```

---

## 📖 Card Management Endpoints

### 13. Get Specific Card
**Endpoint:** `GET /cards/{card_id}`  
**Authentication:** Optional

**Success Response (200):**
```json
{
  "id": "card-uuid",
  "topic_id": "topic-uuid",
  "question": "What is recursion?",
  "answer": "**Recursion** is when a function calls itself",
  "difficulty": 3,
  "concept_tag": "Programming Concepts",
  "card_type": "standard",
  "total_views": 1250,
  "save_rate": 0.15
}
```

### 14. Save Card for Later
**Endpoint:** `POST /cards/{card_id}/save`  
**Authentication:** Required

**Request Body (all fields optional):**
```json
{
  "folder": "Python Basics",
  "tags": ["programming", "fundamentals"],
  "notes": "Important concept for understanding algorithms"
}
```

**Success Response (201 for new, 200 for update):**
```json
{
  "id": "saved-card-uuid",
  "card_id": "card-uuid",
  "saved_at": "2024-01-15T10:30:00Z",
  "folder": "Python Basics",
  "tags": ["programming", "fundamentals"],
  "notes": "Important concept for understanding algorithms",
  "card": {
    "id": "card-uuid",
    "question": "What is recursion?",
    "answer": "**Recursion** is when a function calls itself",
    "difficulty": 3,
    "concept_tag": "Programming Concepts"
  }
}
```

### 15. Remove Card from Saved
**Endpoint:** `DELETE /cards/{card_id}/save`  
**Authentication:** Required

**Success Response (204):** No content

**Error Response (404):**
```json
{
  "detail": "Error in deleting card with the error: Card with ID {card_id} not found in saved list"
}
```

### 16. Get Saved Cards
**Endpoint:** `GET /cards/saved`  
**Authentication:** Required

**Query Parameters:**
- `folder` (optional): Filter by folder name
- `tag` (optional): Filter by tag
- `skip` (optional): Number to skip (default: 0)
- `limit` (optional): Max results (default: 20, max: 100)

**Example Request:**
```
GET /cards/saved?folder=Python%20Basics&skip=0&limit=10
```

**Success Response (200):**
```json
[
  {
    "id": "saved-card-uuid",
    "card_id": "card-uuid",
    "saved_at": "2024-01-15T10:30:00Z",
    "folder": "Python Basics",
    "tags": ["programming", "fundamentals"],
    "notes": "Important concept",
    "card": {
      "id": "card-uuid",
      "question": "What is recursion?",
      "answer": "**Recursion** is when a function calls itself",
      "difficulty": 3,
      "concept_tag": "Programming Concepts"
    }
  }
]
```

---

## 🚨 Error Handling

### Common HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 204 | No Content | Request successful, no content returned |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Invalid or missing authentication |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |

### Error Response Format
```json
{
  "detail": "Detailed error message",
  "error_code": "OPTIONAL_ERROR_CODE",
  "field_errors": {
    "field_name": ["Field-specific error message"]
  }
}
```

---

## 🔧 Frontend Integration Examples

### React Hook for Authentication
```javascript
const useAuth = () => {
  const [token, setToken] = useState(localStorage.getItem('access_token'));

  const login = async (username, password) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    const response = await fetch('/api/v1/auth/token', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();
    setToken(data.access_token);
    localStorage.setItem('access_token', data.access_token);
  };

  return { token, login };
};
```

### API Client Setup
```javascript
const apiClient = {
  baseURL: 'http://localhost:8000/api/v1',
  
  async request(endpoint, options = {}) {
    const token = localStorage.getItem('access_token');
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
        ...options.headers,
      },
      ...options,
    };

    const response = await fetch(`${this.baseURL}${endpoint}`, config);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    return response.json();
  },

  // Learning session methods
  async startSession(topic, mode = 'standard') {
    return this.request('/learning/start', {
      method: 'POST',
      body: JSON.stringify({ topic, mode }),
    });
  },

  async getNextCard(sessionId) {
    return this.request(`/learning/session/${sessionId}/next`);
  },

  async updateMetrics(sessionId, metrics) {
    return this.request(`/learning/session/${sessionId}/metrics`, {
      method: 'POST',
      body: JSON.stringify(metrics),
    });
  },
};
```

### Learning Session Flow
```javascript
const LearningSession = () => {
  const [session, setSession] = useState(null);
  const [currentCard, setCurrentCard] = useState(null);

  const startSession = async (topic) => {
    const sessionData = await apiClient.startSession(topic);
    setSession(sessionData);
    setCurrentCard(sessionData.initial_cards[0]);
  };

  const getNextCard = async () => {
    const card = await apiClient.getNextCard(session.session_id);
    setCurrentCard(card);
  };

  const handleSwipe = async (action, timeSpent) => {
    await apiClient.updateMetrics(session.session_id, {
      card_id: currentCard.id,
      time_spent: timeSpent,
      answer_revealed: true,
      action: action, // 'view', 'skip', 'save', 'master'
    });
    
    await getNextCard();
  };

  return (
    // Your swipe interface component
  );
};
```

---

## 📝 Development Notes

### Rate Limiting
- Default: 60 requests per minute per IP
- Authenticated users may have higher limits
- Rate limit headers included in responses

### Caching
- Topics and cards are cached for better performance
- Cache TTL: 5 minutes for most endpoints
- Use appropriate cache headers in frontend

### Pagination
- Most list endpoints support `skip` and `limit` parameters
- Maximum `limit` is typically 100
- Use cursor-based pagination for large datasets

### Real-time Features
Consider implementing WebSocket connections for:
- Live session updates
- Real-time notifications
- Collaborative learning features

---

## 🧪 Testing Endpoints

Use these curl commands to test the API:

### Test Registration
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"password123"}'
```

### Test Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=password123"
```

### Test Protected Endpoint
```bash
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

This documentation provides a comprehensive guide for frontend developers to integrate with the Infinity Learning Platform API. All endpoints include detailed request/response examples and error handling information.