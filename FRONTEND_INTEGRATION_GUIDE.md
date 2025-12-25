# 📱 Frontend Integration Guide - Journaling Feature

**For:** Frontend Engineer  
**Date:** December 22, 2025  
**Status:** Backend Ready - Start Integration Now!

---

## 🎉 Good News!

The **Journaling backend is fully deployed and tested**! All 12 API endpoints are live and working on production.

---

## 🌐 **API Base URL**

```
Production: http://72.61.170.25:8000
```

All journaling endpoints start with `/journal/`

---

## 🔑 **Quick Start**

### **1. Create a Journal Entry**

```javascript
const createEntry = async (userId, mood, title, content, tags, timeSpent) => {
  const response = await fetch('http://72.61.170.25:8000/journal/entry', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      user_id: userId,
      mood: mood,  // Must be: 😊 😃 😐 😢
      title: title,
      content: content,
      tags: tags,  // Array: ["#calm", "#work"]
      time_spent: timeSpent  // In seconds (e.g., 350)
    })
  });
  
  const data = await response.json();
  
  if (data.success) {
    console.log('Entry saved!', data.entry_id);
    console.log('Streak updated:', data.current_streak);
    return data;
  }
};

// Example usage:
createEntry(
  'user123',
  '😊',
  'My First Journal',
  'Today was amazing!',
  ['#happy', '#success'],
  350  // 5 minutes 50 seconds
);
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

---

### **2. Get Recent Entries**

```javascript
const getRecentEntries = async (userId, limit = 5) => {
  const response = await fetch(
    `http://72.61.170.25:8000/journal/recent-entries?user_id=${userId}&limit=${limit}`
  );
  
  const data = await response.json();
  return data.recent_entries;
};

// Example usage:
const entries = await getRecentEntries('user123', 5);
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
  "total": 2
}
```

---

### **3. Get Daily Prompt**

```javascript
const getDailyPrompt = async () => {
  const response = await fetch('http://72.61.170.25:8000/journal/daily-prompt');
  const data = await response.json();
  return data.prompt;
};

// Example usage:
const prompt = await getDailyPrompt();
console.log(prompt.text);  // "What is one small thing you can control today?"
```

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

---

### **4. Get User's Streak**

```javascript
const getStreak = async (userId) => {
  const response = await fetch(
    `http://72.61.170.25:8000/journal/streak?user_id=${userId}`
  );
  
  const data = await response.json();
  return data.current_streak;
};

// Example usage:
const streak = await getStreak('user123');
console.log(`Current streak: ${streak} days`);
```

**Response:**
```json
{
  "success": true,
  "current_streak": 1
}
```

---

### **5. Toggle Favorite**

```javascript
const toggleFavorite = async (entryId, userId) => {
  const response = await fetch(
    `http://72.61.170.25:8000/journal/favorite/${entryId}?user_id=${userId}`,
    { method: 'POST' }
  );
  
  const data = await response.json();
  return data.is_favorite;
};

// Example usage:
const isFavorite = await toggleFavorite('69492dc618c1962d2ba3bd2e', 'user123');
```

**Response:**
```json
{
  "success": true,
  "is_favorite": true,
  "message": "Added to favorites"
}
```

---

## 📡 **All Available Endpoints**

| Endpoint | Method | Purpose | Required Params |
|----------|--------|---------|-----------------|
| `/journal/entry` | POST | Create entry | user_id, mood, title, content |
| `/journal/recent-entries` | GET | Get last 5 | user_id |
| `/journal/entry/{id}` | GET | Get specific | user_id |
| `/journal/entry/{id}` | PUT | Update | user_id |
| `/journal/entry/{id}` | DELETE | Delete | user_id |
| `/journal/favorite/{id}` | POST | Toggle fav | user_id |
| `/journal/favorites` | GET | All favorites | user_id |
| `/journal/past-reflections` | GET | By date | user_id, date (optional) |
| `/journal/calendar-data` | GET | Calendar | user_id, year, month |
| `/journal/streak` | GET | Current streak | user_id |
| `/journal/daily-prompt` | GET | Random prompt | none |
| `/journal/stats` | GET | Statistics | user_id |

---

## ⚠️ **Important Rules**

### **1. Mood Validation**
Only these 4 emojis are allowed:
- `😊` - Happy
- `😃` - Excited
- `😐` - Neutral
- `😢` - Sad

**Frontend must enforce this!**

### **2. Time Tracking**
- Track time user spends on journaling page
- Send `time_spent` in **seconds**
- Streak updates only if `time_spent >= 300` (5 minutes)

```javascript
let startTime = Date.now();

// When user saves entry:
const timeSpent = Math.floor((Date.now() - startTime) / 1000);
```

### **3. User ID**
- Always send `user_id` in every request
- Use the authenticated user's ID from your auth system

### **4. Tags Format**
- Tags must start with `#`
- Example: `["#calm", "#work", "#happy"]`

---

## 🎨 **UI Integration Tips**

### **For "New Entry" Tab:**

1. **Mood Selector:** 4 emoji buttons (😊 😃 😐 😢)
2. **Title Input:** Text field (min 3 chars)
3. **Content Input:** Textarea (min 10 chars)
4. **Tags Input:** Chip input with `#` prefix
5. **Save Button:** Calls `POST /journal/entry`
6. **Daily Prompt:** Show at top, fetch from `/journal/daily-prompt`

### **For "Recent Entries" Section:**

1. Fetch from `/journal/recent-entries?user_id={id}&limit=5`
2. Display:
   - Date (already formatted: "Today, 11:38 AM")
   - Title
   - Preview (already truncated)
   - Mood emoji
   - Tags
3. Add star icon for favorites (toggle with `/journal/favorite/{id}`)

### **For "Streak" Display:**

1. Fetch from `/journal/streak?user_id={id}`
2. Show: "🔥 {streak} Days"
3. Update after saving entry

### **For "Past Reflections" Tab:**

1. Show calendar (use `/journal/calendar-data`)
2. Dates with entries have dots/highlights
3. Click date → fetch `/journal/past-reflections?user_id={id}&date=2025-12-22`
4. Display all entries for that date

### **For "Favorites" Tab:**

1. Fetch from `/journal/favorites?user_id={id}`
2. Display like recent entries
3. All have filled star icon

---

## 🧪 **Testing**

### **Test User:**
```
user_id: test_user_123
```

### **Test Commands:**
```bash
# Create entry
curl -X POST http://72.61.170.25:8000/journal/entry \
  -H "Content-Type: application/json" \
  -d '{"user_id":"test_user_123","mood":"😊","title":"Test","content":"Testing!","tags":["#test"],"time_spent":350}'

# Get recent
curl "http://72.61.170.25:8000/journal/recent-entries?user_id=test_user_123"

# Get streak
curl "http://72.61.170.25:8000/journal/streak?user_id=test_user_123"
```

---

## 🐛 **Error Handling**

All endpoints return:
```json
{
  "success": true/false,
  "error": "Error message if failed"
}
```

**Handle errors:**
```javascript
const response = await fetch(url);
const data = await response.json();

if (!data.success) {
  console.error('Error:', data.error);
  showErrorToUser(data.error);
}
```

---

## 📊 **Complete Example: Journaling Page**

```javascript
// journaling.js

class JournalingPage {
  constructor(userId) {
    this.userId = userId;
    this.startTime = Date.now();
    this.baseUrl = 'http://72.61.170.25:8000/journal';
  }

  async init() {
    // Load daily prompt
    const prompt = await this.getDailyPrompt();
    this.displayPrompt(prompt);

    // Load recent entries
    const entries = await this.getRecentEntries();
    this.displayRecentEntries(entries);

    // Load streak
    const streak = await this.getStreak();
    this.displayStreak(streak);
  }

  async getDailyPrompt() {
    const res = await fetch(`${this.baseUrl}/daily-prompt`);
    const data = await res.json();
    return data.prompt;
  }

  async getRecentEntries() {
    const res = await fetch(
      `${this.baseUrl}/recent-entries?user_id=${this.userId}&limit=5`
    );
    const data = await res.json();
    return data.recent_entries;
  }

  async getStreak() {
    const res = await fetch(
      `${this.baseUrl}/streak?user_id=${this.userId}`
    );
    const data = await res.json();
    return data.current_streak;
  }

  async saveEntry(mood, title, content, tags) {
    const timeSpent = Math.floor((Date.now() - this.startTime) / 1000);

    const res = await fetch(`${this.baseUrl}/entry`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: this.userId,
        mood,
        title,
        content,
        tags,
        time_spent: timeSpent
      })
    });

    const data = await res.json();

    if (data.success) {
      this.showSuccess(`Entry saved! Streak: ${data.current_streak} days`);
      this.clearForm();
      this.init(); // Refresh data
    } else {
      this.showError(data.error);
    }
  }

  async toggleFavorite(entryId) {
    const res = await fetch(
      `${this.baseUrl}/favorite/${entryId}?user_id=${this.userId}`,
      { method: 'POST' }
    );
    const data = await res.json();
    return data.is_favorite;
  }

  // UI methods...
  displayPrompt(prompt) { /* ... */ }
  displayRecentEntries(entries) { /* ... */ }
  displayStreak(streak) { /* ... */ }
  showSuccess(msg) { /* ... */ }
  showError(msg) { /* ... */ }
  clearForm() { /* ... */ }
}

// Usage:
const journaling = new JournalingPage(currentUser.id);
journaling.init();
```

---

## 📝 **Checklist for Frontend**

- [ ] Create entry form (mood, title, content, tags)
- [ ] Track time spent on page
- [ ] Display daily prompt
- [ ] Show recent entries (5)
- [ ] Display current streak
- [ ] Implement favorites toggle
- [ ] Create past reflections view (calendar)
- [ ] Add favorites tab
- [ ] Handle all error cases
- [ ] Test with real user IDs
- [ ] Validate mood emojis
- [ ] Format tags with `#`

---

## 🚀 **Ready to Start!**

Everything is deployed and tested. You can start integrating immediately!

**Questions?** Check:
- Full API docs: `journaling/README.md`
- Technical details: `journaling/TECHNICAL_DEEP_DIVE.md`

**Need help?** The backend team is available!

---

*Backend deployed: December 22, 2025*  
*Status: Production Ready ✅*
