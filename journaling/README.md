# 📝 Journaling Module - Backend Implementation

Complete backend implementation for the Journaling feature in the Mental Health App.

---

## 📁 Module Structure

```
journaling/
├── __init__.py          # Module initialization
├── models.py            # Pydantic data models
├── database.py          # MongoDB setup and collections
├── service.py           # Business logic
├── routes.py            # FastAPI endpoints
└── README.md            # This file
```

---

## 🚀 Features Implemented

### ✅ Core Features
1. **Create Journal Entry** - Save mood, title, content, tags
2. **Recent Entries** - Get last 5 entries with formatted dates
3. **Past Reflections** - View entries by date
4. **Calendar View** - See which dates have entries
5. **Favorites** - Mark/unmark entries as favorites
6. **Streak Tracking** - Auto-update streak (5+ min sessions)
7. **Daily Prompts** - Random journaling prompts
8. **Statistics** - Comprehensive user stats

### ✅ Database Collections
- `journal_entries` - All journal entries
- `journal_streaks` - User streak data
- `daily_prompts` - Journaling prompts (pre-seeded)

---

## 🔌 Integration with Main App

### Step 1: Import in `langraph_tool.py`

Add at the top of `langraph_tool.py`:

```python
# Import journaling module
from journaling import router as journaling_router, init_journaling_db
```

### Step 2: Initialize Database

In the `init_db()` function, add:

```python
async def init_db():
    global client, chats_col, marks_col, reports_col, router_memory_col
    
    # Existing code...
    
    # Initialize journaling database
    await init_journaling_db(client, DB_NAME)
    
    logger.info("✅ All databases initialized")
```

### Step 3: Register Routes

After creating the FastAPI app, add:

```python
app = FastAPI(lifespan=lifespan)

# Include journaling routes
app.include_router(journaling_router)

# Existing routes...
```

---

## 📡 API Endpoints

### **1. Create Entry**
```http
POST /journal/entry
Content-Type: application/json

{
  "user_id": "user123",
  "mood": "😊",
  "title": "Finding stillness in chaos",
  "content": "Today was overwhelming at work...",
  "tags": ["#calm", "#work"],
  "time_spent": 320
}

Response:
{
  "success": true,
  "entry_id": "entry123",
  "message": "Journal entry saved successfully",
  "streak_updated": true,
  "current_streak": 13
}
```

### **2. Get Recent Entries**
```http
GET /journal/recent-entries?user_id=user123&limit=5

Response:
{
  "success": true,
  "recent_entries": [
    {
      "id": "entry123",
      "date": "Yesterday, 5:20 PM",
      "timestamp": "2025-12-21T17:20:00Z",
      "title": "Finding stillness in chaos",
      "preview": "Today was overwhelming at work...",
      "mood": "😊",
      "tags": ["#calm"],
      "time_spent": 320,
      "is_favorite": false
    }
  ],
  "total": 1
}
```

### **3. Get Entry by ID**
```http
GET /journal/entry/{entry_id}?user_id=user123

Response:
{
  "success": true,
  "entry": {
    "id": "entry123",
    "user_id": "user123",
    "mood": "😊",
    "title": "Finding stillness in chaos",
    "content": "Full content here...",
    "tags": ["#calm"],
    "time_spent": 320,
    "is_favorite": false,
    "timestamp": "2025-12-21T17:20:00Z"
  }
}
```

### **4. Update Entry**
```http
PUT /journal/entry/{entry_id}
Content-Type: application/json

{
  "user_id": "user123",
  "title": "Updated title",
  "content": "Updated content"
}

Response:
{
  "success": true,
  "message": "Entry updated successfully"
}
```

### **5. Delete Entry**
```http
DELETE /journal/entry/{entry_id}?user_id=user123

Response:
{
  "success": true,
  "message": "Entry deleted successfully"
}
```

### **6. Toggle Favorite**
```http
POST /journal/favorite/{entry_id}?user_id=user123

Response:
{
  "success": true,
  "is_favorite": true,
  "message": "Added to favorites"
}
```

### **7. Get Favorites**
```http
GET /journal/favorites?user_id=user123

Response:
{
  "success": true,
  "favorites": [...],
  "total": 5
}
```

### **8. Get Past Reflections**
```http
GET /journal/past-reflections?user_id=user123&date=2025-12-22

Response:
{
  "success": true,
  "date": "2025-12-22",
  "entries": [...],
  "total_entries": 2,
  "total_time_spent": 640
}
```

### **9. Get Calendar Data**
```http
GET /journal/calendar-data?user_id=user123&year=2025&month=12

Response:
{
  "success": true,
  "month": "2025-12",
  "dates_with_entries": [
    {
      "date": "2025-12-22",
      "count": 2,
      "mood": "😊"
    }
  ]
}
```

### **10. Get Streak**
```http
GET /journal/streak?user_id=user123

Response:
{
  "success": true,
  "current_streak": 13
}
```

### **11. Get Daily Prompt**
```http
GET /journal/daily-prompt

Response:
{
  "success": true,
  "prompt": {
    "prompt_id": "prompt_001",
    "text": "What is one small thing you can control today?",
    "category": "reflection"
  }
}
```

### **12. Get Statistics**
```http
GET /journal/stats?user_id=user123

Response:
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

## 🎯 Streak Logic

### How Streaks Work:

1. **Entry Created** → Check `time_spent`
2. **If ≥ 5 minutes (300 seconds)** → Update streak
3. **Check Last Entry Date:**
   - **Today** → Don't update (already counted)
   - **Yesterday** → Increment streak
   - **Older** → Reset streak to 1
4. **Update Longest Streak** if current > longest

### Streak Validation:

```python
# Streak is valid if last entry was today or yesterday
if last_entry_date in [today, yesterday]:
    return current_streak
else:
    return 0  # Streak broken
```

---

## 📊 Database Schema

### **journal_entries**
```javascript
{
  "_id": ObjectId,
  "user_id": "user123",
  "mood": "😊",
  "title": "Finding stillness in chaos",
  "content": "Full journal entry text...",
  "tags": ["#calm", "#work"],
  "time_spent": 320,  // seconds
  "is_favorite": false,
  "favorited_at": null,  // or ISODate
  "timestamp": ISODate("2025-12-21T17:20:00Z"),
  "created_at": ISODate("2025-12-21T17:20:00Z"),
  "updated_at": ISODate("2025-12-21T17:20:00Z")
}
```

### **journal_streaks**
```javascript
{
  "_id": ObjectId,
  "user_id": "user123",
  "current_streak": 13,
  "last_entry_date": ISODate("2025-12-22"),
  "longest_streak": 21,
  "total_days": 45,
  "created_at": ISODate("2025-12-01T00:00:00Z"),
  "updated_at": ISODate("2025-12-22T10:30:00Z")
}
```

### **daily_prompts**
```javascript
{
  "_id": ObjectId,
  "prompt_id": "prompt_001",
  "text": "What is one small thing you can control today?",
  "category": "reflection",
  "active": true,
  "created_at": ISODate("2025-12-01T00:00:00Z")
}
```

---

## 🔍 Indexes Created

For optimal performance:

```python
# journal_entries
- user_id (single)
- timestamp (single)
- (user_id, timestamp) (compound, descending)
- (user_id, is_favorite) (compound)
- tags (single)

# journal_streaks
- user_id (unique)

# daily_prompts
- prompt_id (unique)
- active (single)
```

---

## 🧪 Testing

### Test Create Entry:
```bash
curl -X POST http://localhost:8000/journal/entry \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "mood": "😊",
    "title": "Test Entry",
    "content": "This is a test journal entry to verify the backend works.",
    "tags": ["#test"],
    "time_spent": 350
  }'
```

### Test Get Recent:
```bash
curl http://localhost:8000/journal/recent-entries?user_id=test_user
```

### Test Streak:
```bash
curl http://localhost:8000/journal/streak?user_id=test_user
```

---

## 📝 Frontend Integration

### Example: Create Entry

```javascript
// Frontend code
async function saveJournalEntry(entryData) {
  const response = await fetch('http://72.61.170.25:8000/journal/entry', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      user_id: currentUser.id,
      mood: selectedMood,
      title: titleInput.value,
      content: contentInput.value,
      tags: selectedTags,
      time_spent: sessionDuration  // in seconds
    })
  });
  
  const result = await response.json();
  
  if (result.success) {
    // Show success message
    showNotification(`Entry saved! Streak: ${result.current_streak} days`);
    
    // Update UI
    updateRecentEntries();
    updateStreakDisplay(result.current_streak);
    
    // Clear form
    clearEntryForm();
  }
}
```

---

## 🚀 Deployment

### On VPS:

1. **Upload journaling folder** to `/root/app/journaling/`

2. **Update langraph_tool.py** with integration code

3. **Restart service:**
```bash
sudo systemctl restart fastapi
```

4. **Check logs:**
```bash
sudo journalctl -u fastapi -f | grep journaling
```

5. **Test endpoints:**
```bash
curl http://localhost:8000/journal/daily-prompt
```

---

## ⚠️ Important Notes

1. **Time Tracking:** Frontend must track time spent and send `time_spent` in seconds
2. **Mood Validation:** Only accept: 😊 😃 😐 😢
3. **Streak Updates:** Only count if `time_spent >= 300` (5 minutes)
4. **Date Formatting:** Backend handles all date formatting
5. **User ID:** Always required in requests

---

## 🎯 Next Steps

1. ✅ Backend complete
2. ⏳ Frontend integration
3. ⏳ Testing with real users
4. ⏳ Analytics dashboard
5. ⏳ Export journal entries (PDF/JSON)

---

## 📞 Support

For issues or questions:
- Check logs: `sudo journalctl -u fastapi -f`
- Review `TROUBLESHOOTING_REPORT.md`
- Test endpoints with curl/Postman

---

*Last Updated: December 22, 2025*  
*Module Version: 1.0*
