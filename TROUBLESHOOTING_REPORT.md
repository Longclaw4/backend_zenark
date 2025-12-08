# 🔧 Troubleshooting Guide: Report Generation 500 Error

## Problem
The `/generate_report` endpoint is returning a 500 error when triggered from the app.

---

## Step-by-Step Debugging Process

### Step 1: Access the VPS and View Live Logs

1. **SSH into the server:**
   ```bash
   ssh root@72.61.170.25
   ```
   Password: `GenericPassword123#`

2. **Start watching live logs:**
   ```bash
   sudo journalctl -u fastapi -f
   ```
   Keep this terminal open.

3. **Trigger the report generation** from your app or Postman.

4. **Read the error message** in the terminal. It will show the exact Python traceback.

---

## Common Issues and Solutions

### Issue 1: Database Not Initialized
**Error message:** `"Database not initialized"`

**Solution:**
```bash
# Check if MongoDB is accessible
cd /root/app
python3 << EOF
import os
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

async def test_db():
    mongo_uri = os.getenv('MONGO_DB_OFFICIAL')
    print(f"Testing connection to: {mongo_uri[:20]}...")
    client = AsyncIOMotorClient(mongo_uri)
    try:
        await client.admin.command('ping')
        print("✓ MongoDB connection successful!")
    except Exception as e:
        print(f"✗ MongoDB connection failed: {e}")

asyncio.run(test_db())
EOF
```

**If connection fails:**
- Check `.env` file has correct `MONGO_DB_OFFICIAL` value
- Verify MongoDB Atlas IP whitelist includes VPS IP (72.61.170.25)
- Check MongoDB user credentials

---

### Issue 2: No Conversation Found
**Error message:** `"No conversation found for user in this session"`

**Cause:** The `chats` collection doesn't have data for this user/session.

**Solution:**
```bash
# Check if chats collection has data
cd /root/app
python3 << EOF
import os
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

async def check_chats():
    mongo_uri = os.getenv('MONGO_DB_OFFICIAL')
    db_name = os.getenv('MONGO_DB_NAME_OFFICIAL')
    client = AsyncIOMotorClient(mongo_uri)
    db = client[db_name]
    
    count = await db.chats.count_documents({})
    print(f"Total chats in database: {count}")
    
    if count > 0:
        sample = await db.chats.find_one()
        print(f"Sample chat structure: {list(sample.keys())}")

asyncio.run(check_chats())
EOF
```

**If no chats found:**
- User needs to have a conversation first before generating report
- Check if chat messages are being saved correctly

---

### Issue 3: OpenAI API Key Issues
**Error message:** `"AuthenticationError"` or `"RateLimitError"`

**Solution:**
```bash
# Check if API key is set
cd /root/app
grep OPENAI_API_KEY .env

# Test API key
python3 << EOF
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "test"}],
        max_tokens=5
    )
    print("✓ OpenAI API key is valid!")
except Exception as e:
    print(f"✗ OpenAI API error: {e}")
EOF
```

**If API key invalid:**
- Update `.env` file with valid key
- Restart service: `sudo systemctl restart fastapi`

---

### Issue 4: Missing `generate_autogen_report` Function
**Error message:** `"NameError: name 'generate_autogen_report' is not defined"`

**Solution:**
```bash
# Check if autogen_report.py exists
cd /root/app
ls -la autogen_report.py

# Check if it's imported in langraph_tool.py
grep "from autogen_report import" langraph_tool.py
```

**If missing:**
- Ensure `autogen_report.py` is in the repo
- Add import: `from autogen_report import generate_autogen_report`
- Restart service

---

### Issue 5: Memory/Timeout Issues
**Error message:** `"TimeoutError"` or service crashes

**Solution:**
```bash
# Check server resources
htop  # Press 'q' to quit

# Check if service has memory limits
sudo systemctl show fastapi | grep Memory

# Increase timeout in service file
sudo nano /etc/systemd/system/fastapi.service
```

Add to `[Service]` section:
```
TimeoutStartSec=300
TimeoutStopSec=300
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl restart fastapi
```

---

### Issue 6: `session_id` Undefined Error
**Error message:** `"UnboundLocalError: local variable 'session_id' referenced before assignment"`

**Cause:** Line 2435 in `langraph_tool.py` uses `session_id` but it's only defined inside the `if latest_chat` block.

**Solution:**
```bash
cd /root/app
nano langraph_tool.py
```

Find line ~2405 and add:
```python
session_id = None  # Initialize before the if block
```

Or edit the code to handle the case when `session_id` is not found.

---

## Step 2: Enable Debug Mode

Add more logging to see exactly where it fails:

```bash
cd /root/app
nano langraph_tool.py
```

In the `generate_report_endpoint` function, add print statements:

```python
@app.post("/generate_report")
async def generate_report_endpoint(req: ReportRequest):
    print("🔍 DEBUG: Starting report generation")
    try:
        payload = decode_jwt(req.token)
        user_id = payload.get("id")
        print(f"🔍 DEBUG: User ID: {user_id}")
        
        # ... rest of code ...
        
        print(f"🔍 DEBUG: Session ID: {session_id}")
        print(f"🔍 DEBUG: Score: {score}")
        
        report_data = await generate_report(user_id_obj, session_id, score)
        print(f"🔍 DEBUG: Report generated: {bool(report_data)}")
        
        # ... rest of code ...
```

Save, then restart:
```bash
sudo systemctl restart fastapi
sudo journalctl -u fastapi -f
```

---

## Step 3: Test Endpoint Manually

Create a test script:

```bash
cd /root/app
cat > test_report.py << 'EOF'
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

async def test_report():
    # Initialize DB
    mongo_uri = os.getenv('MONGO_DB_OFFICIAL')
    db_name = os.getenv('MONGO_DB_NAME_OFFICIAL')
    client = AsyncIOMotorClient(mongo_uri)
    db = client[db_name]
    
    # Get a sample user with chats
    chat = await db.chats.find_one({})
    if not chat:
        print("No chats found in database")
        return
    
    user_id = chat.get('userId')
    session_id = chat.get('session_id')
    
    print(f"Testing with user_id: {user_id}, session_id: {session_id}")
    
    # Test the generate_report function
    from langraph_tool import generate_report
    result = await generate_report(user_id, session_id, 5)
    print(f"Result: {result}")

asyncio.run(test_report())
EOF

python3 test_report.py
```

---

## Step 4: Check Service Configuration

```bash
# View full service configuration
sudo systemctl cat fastapi

# Check if workers are configured
grep -i "workers" /etc/systemd/system/fastapi.service
```

---

## Quick Fix Checklist

- [ ] MongoDB connection is working
- [ ] `chats` collection has data
- [ ] `reports` collection exists
- [ ] OpenAI API key is valid and has credits
- [ ] `autogen_report.py` exists and is imported
- [ ] `session_id` variable is properly initialized
- [ ] Service has enough memory (check with `htop`)
- [ ] No syntax errors in code (`python3 -m py_compile langraph_tool.py`)
- [ ] Environment variables are loaded (check `.env` file)

---

## Get Help

If none of the above works, collect this information:

```bash
# 1. Full error log
sudo journalctl -u fastapi -n 100 --no-pager > error_log.txt

# 2. Service status
sudo systemctl status fastapi > service_status.txt

# 3. Environment check
env | grep -E "MONGO|OPENAI|HF" > env_vars.txt

# 4. Code version
cd /root/app
git log -1 > git_version.txt
```

Then share these files for debugging.
