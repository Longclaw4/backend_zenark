# 🔌 Journaling Module - Integration Guide

Quick guide to integrate the journaling module into `langraph_tool.py`

---

## Step 1: Add Import Statements

At the top of `langraph_tool.py`, add:

```python
# Journaling Module
from journaling import router as journaling_router, init_journaling_db
```

---

## Step 2: Initialize Database

In the `init_db()` function, add journaling initialization:

```python
async def init_db():
    """Initialize MongoDB collections asynchronously using Motor."""
    global client, chats_col, marks_col, reports_col, router_memory_col
    
    try:
        MONGO_URI = os.getenv('MONGO_DB_OFFICIAL')
        DB_NAME = os.getenv('MONGO_DB_NAME_OFFICIAL')
        
        if not MONGO_URI or not DB_NAME:
            raise ValueError("MongoDB configuration missing")
        
        client = AsyncIOMotorClient(MONGO_URI)
        db = client[DB_NAME]
        
        # Existing collections
        chats_col = db["chat_sessions"]
        marks_col = db["student_marks"]
        reports_col = db["reports"]
        router_memory_col = db["router_memory"]
        
        # ✅ NEW: Initialize journaling database
        await init_journaling_db(client, DB_NAME)
        
        logger.info("✅ All databases initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise
```

---

## Step 3: Register Routes

After creating the FastAPI app, include the journaling router:

```python
# Create FastAPI app
app = FastAPI(lifespan=lifespan)

# ✅ NEW: Include journaling routes
app.include_router(journaling_router)

# Existing routes
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# ... rest of your routes
```

---

## Step 4: Test the Integration

### 4.1 Restart the Service

```bash
# On VPS
sudo systemctl restart fastapi
```

### 4.2 Check Logs

```bash
sudo journalctl -u fastapi -f
```

Look for:
```
✅ Journaling database initialized successfully
✅ Seeded 10 daily prompts
```

### 4.3 Test Endpoints

```bash
# Test daily prompt
curl http://localhost:8000/journal/daily-prompt

# Test health (should still work)
curl http://localhost:8000/health
```

---

## Step 5: Verify Database

```bash
# Connect to MongoDB (if you have mongo shell)
mongo "YOUR_MONGO_URI"

# Check collections
use zenark_db
show collections

# Should see:
# - journal_entries
# - journal_streaks
# - daily_prompts
```

---

## Complete Integration Code

Here's the complete code to add to `langraph_tool.py`:

```python
# ============================================
# AT THE TOP (with other imports)
# ============================================

from journaling import router as journaling_router, init_journaling_db


# ============================================
# IN init_db() FUNCTION
# ============================================

async def init_db():
    global client, chats_col, marks_col, reports_col, router_memory_col
    
    try:
        MONGO_URI = os.getenv('MONGO_DB_OFFICIAL')
        DB_NAME = os.getenv('MONGO_DB_NAME_OFFICIAL')
        
        if not MONGO_URI or not DB_NAME:
            raise ValueError("MongoDB configuration missing")
        
        client = AsyncIOMotorClient(MONGO_URI)
        db = client[DB_NAME]
        
        chats_col = db["chat_sessions"]
        marks_col = db["student_marks"]
        reports_col = db["reports"]
        router_memory_col = db["router_memory"]
        
        # Initialize journaling
        await init_journaling_db(client, DB_NAME)
        
        logger.info("✅ All databases initialized")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise


# ============================================
# AFTER app = FastAPI(lifespan=lifespan)
# ============================================

app = FastAPI(lifespan=lifespan)

# Include journaling routes
app.include_router(journaling_router)

# ... rest of your app code
```

---

## Troubleshooting

### Issue: Import Error

```
ModuleNotFoundError: No module named 'journaling'
```

**Solution:** Make sure the `journaling` folder is in the same directory as `langraph_tool.py`

```bash
# Check structure
ls -la /root/app/
# Should see:
# - langraph_tool.py
# - journaling/
```

---

### Issue: Database Not Initialized

```
RuntimeError: Journaling database not initialized
```

**Solution:** Make sure `init_journaling_db()` is called in `init_db()`

---

### Issue: Routes Not Found

```
404 Not Found: /journal/daily-prompt
```

**Solution:** Make sure `app.include_router(journaling_router)` is called

---

## Verification Checklist

- [ ] `journaling` folder exists in `/root/app/`
- [ ] Import statement added to `langraph_tool.py`
- [ ] `init_journaling_db()` called in `init_db()`
- [ ] `app.include_router(journaling_router)` added
- [ ] Service restarted
- [ ] Logs show "Journaling database initialized"
- [ ] Test endpoint works: `/journal/daily-prompt`

---

## Next Steps

1. ✅ Backend integrated
2. ⏳ Connect frontend to endpoints
3. ⏳ Test with real users
4. ⏳ Monitor performance

---

*Integration Guide v1.0*  
*Last Updated: December 22, 2025*
