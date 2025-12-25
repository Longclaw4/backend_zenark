# 📚 Mental Health Chat API Documentation

**Base URL:** `http://72.61.170.25:8000`  
**Version:** 1.0.0  
**Protocol:** HTTP/HTTPS  
**Format:** JSON

---

## 🔗 Interactive Documentation

Once the server is online:

- **Swagger UI:** http://72.61.170.25:8000/docs
- **ReDoc:** http://72.61.170.25:8000/redoc
- **OpenAPI Schema:** http://72.61.170.25:8000/openapi.json

---

## 🔐 Authentication

Most endpoints require JWT authentication.

**Header:**
```
Authorization: Bearer <JWT_TOKEN>
```

---

## 📡 Endpoints Overview

### **Health & Status**

#### `GET /health`
Check server health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-23T15:53:12.123456"
}
```

---

### **Chat Endpoints**

#### `POST /chat`
Main chat endpoint for student-AI conversation.

**Request:**
```json
{
  "message": "I'm feeling stressed about exams",
  "session_id": "session_123",
  "student_id": "user_456",
  "token": "JWT_TOKEN_HERE"
}
```

**Response:**
```json
{
  "response": "I understand exam stress can be overwhelming...",
  "emotion": "negative",
  "tool_used": "negative_conversation_handler",
  "session_id": "session_123"
}
```

**Fields:**
- `message` (string, required): User's message
- `session_id` (string, required): Session identifier
- `student_id` (string, required): User identifier
- `token` (string, required): JWT authentication token

---

### **Report Generation**

#### `POST /generate_report`
Generate mental health report for a student.

**Request:**
```json
{
  "token": "JWT_TOKEN_HERE"
}
```

**Response:**
```json
{
  "userId": "user_456",
  "session_id": "session_123",
  "score": 3,
  "status": "Healthy",
  "report": "Student is coping well with academic pressure...",
  "recommendations": [
    "Continue regular check-ins",
    "Maintain current coping strategies"
  ],
  "timestamp": "2025-12-23T15:53:12.123456"
}
```

**Score Scale (1-10):**
- 1-3: Healthy (Green)
- 4-6: Moderate Concern (Yellow)
- 7-10: Needs Support (Red)

**Note:** Lower scores = Better mental health

---

### **Journaling Endpoints**

#### `POST /journal/entry`
Create a new journal entry.

**Request:**
```json
{
  "user_id": "user_123",
  "mood": "😊",
  "title": "My First Journal",
  "content": "Today was amazing!",
  "tags": ["#happy", "#success"],
  "time_spent": 350
}
```

**Response:**
```json
{
  "success": true,
  "entry_id": "69492dc618c1962d2ba3bd2e",
  "message": "Journal entry saved successfully",
  "streak_updated": true,
  "current_streak": 1
}
```

**Validation:**
- `mood`: Must be one of: 😊 😃 😐 😢
- `time_spent`: In seconds (streak updates if ≥300)
- `tags`: Must start with #

---

#### `GET /journal/recent-entries`
Get user's recent journal entries.

**Parameters:**
- `user_id` (required): User identifier
- `limit` (optional): Number of entries (default: 5)

**Example:**
```
GET /journal/recent-entries?user_id=user_123&limit=5
```

**Response:**
```json
{
  "success": true,
  "recent_entries": [
    {
      "id": "69492dc618c1962d2ba3bd2e",
      "date": "Today, 11:38 AM",
      "timestamp": "2025-12-22T11:38:46.159000",
      "title": "My First Journal",
      "preview": "Today was amazing!",
      "mood": "😊",
      "tags": ["#success"],
      "time_spent": 350,
      "is_favorite": false
    }
  ],
  "total": 1
}
```

---

#### `GET /journal/entry/{entry_id}`
Get a specific journal entry.

**Parameters:**
- `entry_id` (path): Entry identifier
- `user_id` (query): User identifier

**Example:**
```
GET /journal/entry/69492dc618c1962d2ba3bd2e?user_id=user_123
```

**Response:**
```json
{
  "success": true,
  "entry": {
    "id": "69492dc618c1962d2ba3bd2e",
    "user_id": "user_123",
    "mood": "😊",
    "title": "My First Journal",
    "content": "Full content here...",
    "tags": ["#success"],
    "time_spent": 350,
    "is_favorite": false,
    "timestamp": "2025-12-22T11:38:46.159000",
    "created_at": "2025-12-22T11:38:46.159000",
    "updated_at": "2025-12-22T11:38:46.159000"
  }
}
```

---

#### `PUT /journal/entry/{entry_id}`
Update an existing journal entry.

**Request:**
```json
{
  "user_id": "user_123",
  "mood": "😃",
  "title": "Updated Title",
  "content": "Updated content",
  "tags": ["#updated"]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Entry updated successfully"
}
```

---

#### `DELETE /journal/entry/{entry_id}`
Delete a journal entry.

**Parameters:**
- `entry_id` (path): Entry identifier
- `user_id` (query): User identifier

**Response:**
```json
{
  "success": true,
  "message": "Entry deleted successfully"
}
```

---

#### `POST /journal/favorite/{entry_id}`
Toggle favorite status of an entry.

**Parameters:**
- `entry_id` (path): Entry identifier
- `user_id` (query): User identifier

**Response:**
```json
{
  "success": true,
  "is_favorite": true,
  "message": "Added to favorites"
}
```

---

#### `GET /journal/favorites`
Get all favorite entries.

**Parameters:**
- `user_id` (query): User identifier

**Response:**
```json
{
  "success": true,
  "favorites": [
    {
      "id": "entry_id",
      "date": "Yesterday, 5:20 PM",
      "title": "Favorite Entry",
      "preview": "This is my favorite...",
      "mood": "😊",
      "tags": ["#important"],
      "favorited_at": "2025-12-22T17:20:00Z"
    }
  ],
  "total": 1
}
```

---

#### `GET /journal/past-reflections`
Get entries for a specific date.

**Parameters:**
- `user_id` (required): User identifier
- `date` (optional): Date in YYYY-MM-DD format (default: today)

**Example:**
```
GET /journal/past-reflections?user_id=user_123&date=2025-12-22
```

**Response:**
```json
{
  "success": true,
  "date": "2025-12-22",
  "entries": [
    {
      "id": "entry_id",
      "time": "11:38 AM",
      "title": "Morning Reflection",
      "preview": "Started the day well...",
      "mood": "😊",
      "tags": ["#morning"],
      "time_spent": 300,
      "is_favorite": false
    }
  ],
  "total_entries": 1,
  "total_time_spent": 300
}
```

---

#### `GET /journal/calendar-data`
Get calendar data showing dates with entries.

**Parameters:**
- `user_id` (required): User identifier
- `year` (required): Year (e.g., 2025)
- `month` (required): Month (1-12)

**Example:**
```
GET /journal/calendar-data?user_id=user_123&year=2025&month=12
```

**Response:**
```json
{
  "success": true,
  "month": "2025-12",
  "dates_with_entries": [
    {
      "date": "2025-12-22",
      "count": 2,
      "mood": "😊"
    },
    {
      "date": "2025-12-23",
      "count": 1,
      "mood": "😃"
    }
  ]
}
```

---

#### `GET /journal/streak`
Get user's current journaling streak.

**Parameters:**
- `user_id` (required): User identifier

**Response:**
```json
{
  "success": true,
  "current_streak": 13
}
```

**Streak Rules:**
- Updates only if time_spent ≥ 300 seconds (5 minutes)
- Counts consecutive days
- Resets if a day is missed

---

#### `GET /journal/daily-prompt`
Get a random daily journaling prompt.

**No parameters required**

**Response:**
```json
{
  "success": true,
  "prompt": {
    "prompt_id": "prompt_006",
    "text": "What challenge are you facing, and what's one step you can take?",
    "category": "reflection"
  }
}
```

**Prompt Categories:**
- reflection
- gratitude
- goals
- emotions

---

#### `GET /journal/stats`
Get comprehensive user journaling statistics.

**Parameters:**
- `user_id` (required): User identifier

**Response:**
```json
{
  "success": true,
  "stats": {
    "total_entries": 45,
    "current_streak": 13,
    "longest_streak": 21,
    "total_days": 45,
    "mood_distribution": {
      "😊": 20,
      "😃": 15,
      "😐": 8,
      "😢": 2
    },
    "most_used_tags": [
      {"tag": "#calm", "count": 15},
      {"tag": "#focus", "count": 12}
    ],
    "total_time_spent": 13500,
    "average_time_per_entry": 300
  }
}
```

---

### **Analytics Endpoints**

#### `GET /analytics/active_users`
Get count of active users.

**Response:**
```json
{
  "active_users": 42,
  "timestamp": "2025-12-23T15:53:12.123456"
}
```

---

#### `GET /analytics/dashboard`
Get analytics dashboard data.

**Response:**
```json
{
  "status": "success",
  "metrics": {
    "total_users": 150,
    "total_conversations": 1250,
    "total_reports": 45,
    "active_last_24h": 32,
    "average_distress_score": 3.2
  },
  "peak_hours": [
    {"hour": "14:00", "activity_count": 45},
    {"hour": "20:00", "activity_count": 38}
  ],
  "timestamp": "2025-12-23T15:53:12.123456"
}
```

---

## 🔄 Error Responses

All endpoints return errors in this format:

```json
{
  "success": false,
  "error": "Error message here",
  "detail": "Additional details if available"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `400` - Bad Request (invalid input)
- `401` - Unauthorized (invalid/missing token)
- `404` - Not Found
- `500` - Internal Server Error

---

## 📊 Data Models

### **JournalEntry**
```typescript
{
  user_id: string;
  mood: "😊" | "😃" | "😐" | "😢";
  title: string;
  content: string;
  tags: string[];  // Must start with #
  time_spent: number;  // In seconds
  is_favorite: boolean;
  timestamp: string;  // ISO 8601
  created_at: string;  // ISO 8601
  updated_at: string;  // ISO 8601
}
```

### **MentalHealthReport**
```typescript
{
  userId: string;
  session_id: string;
  score: number;  // 1-10 (lower = better)
  status: "Healthy" | "Moderate Concern" | "Needs Support";
  report: string;
  recommendations: string[];
  timestamp: string;  // ISO 8601
}
```

---

## 🧪 Testing

### **Using cURL:**

```bash
# Health check
curl http://72.61.170.25:8000/health

# Create journal entry
curl -X POST http://72.61.170.25:8000/journal/entry \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "mood": "😊",
    "title": "Test",
    "content": "Testing API",
    "tags": ["#test"],
    "time_spent": 350
  }'

# Get recent entries
curl "http://72.61.170.25:8000/journal/recent-entries?user_id=test_user"
```

### **Using JavaScript:**

```javascript
// Create entry
const response = await fetch('http://72.61.170.25:8000/journal/entry', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    user_id: 'user_123',
    mood: '😊',
    title: 'My Journal',
    content: 'Today was great!',
    tags: ['#happy'],
    time_spent: 350
  })
});

const data = await response.json();
console.log(data);
```

---

## 📞 Support

**Documentation:**
- Swagger UI: http://72.61.170.25:8000/docs (when server is online)
- Frontend Guide: `FRONTEND_INTEGRATION_GUIDE.md`
- Journaling Docs: `journaling/README.md`

**Issues:**
- Check server status: `GET /health`
- View logs on VPS
- Contact backend team

---

## 🔄 Rate Limiting

Currently no rate limiting implemented.  
Recommended: 100 requests/minute per user.

---

## 🌐 CORS

CORS is enabled for:
- `https://zenark-app.vercel.app`
- `http://localhost:3000`
- `http://localhost:8081`
- All origins (`*`)

---

## 📝 Notes

1. **Server Status:** Currently offline (infrastructure issue)
2. **Authentication:** JWT required for most endpoints
3. **Mood Validation:** Only 4 emojis allowed
4. **Streak Logic:** Requires 5+ minutes of journaling
5. **Date Format:** All timestamps in ISO 8601

---

*Last Updated: December 23, 2025*  
*API Version: 1.0.0*
