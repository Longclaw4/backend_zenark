# 🚀 VPS Deployment Checklist

## ✅ Pre-Deployment (Local Machine)

- [ ] **Test the code locally** to ensure it works
  ```bash
  python langraph_tool.py
  ```

- [ ] **Commit and push changes to GitHub**
  ```bash
  git add .
  git commit -m "Fix: session_id UnboundLocalError in generate_report endpoint"
  git push origin main
  ```

- [ ] **Verify push was successful**
  - Check GitHub repository to confirm latest commit is visible

---

## 🔧 Deployment to VPS

### Option 1: Using the Automated Script (Recommended)

1. **Connect to VPS**
   - Double-click `connect_vps.bat` (Windows)
   - OR run: `ssh root@72.61.170.25`
   - Password: `GenericPassword123#`

2. **Upload and run deployment script**
   ```bash
   # Navigate to app directory
   cd /root/app  # (or wherever your app is)
   
   # Upload deploy_vps.sh from local machine (use SCP or paste content)
   # OR create it directly on VPS:
   nano deploy_vps.sh
   # (Paste the content from deploy_vps.sh, save with Ctrl+O, exit with Ctrl+X)
   
   # Make it executable
   chmod +x deploy_vps.sh
   
   # Run it
   ./deploy_vps.sh
   ```

### Option 2: Manual Deployment

1. **SSH into VPS**
   ```bash
   ssh root@72.61.170.25
   ```

2. **Navigate to app directory**
   ```bash
   cd /root/app  # Change if different
   ```

3. **Pull latest code**
   ```bash
   git pull origin main
   ```

4. **Install/update dependencies** (if requirements.txt changed)
   ```bash
   pip install -r requirements.txt --upgrade
   ```

5. **Restart the service**
   ```bash
   sudo systemctl restart fastapi
   ```

6. **Check service status**
   ```bash
   sudo systemctl status fastapi
   ```

7. **View logs to confirm no errors**
   ```bash
   sudo journalctl -u fastapi -n 50 --no-pager
   ```

---

## 🧪 Post-Deployment Testing

- [ ] **Health check**
  ```bash
  curl http://72.61.170.25:8000/health
  ```
  Expected: `{"status":"healthy","timestamp":"..."}`

- [ ] **Test chat endpoint** (from Postman or frontend)
  - Endpoint: `POST http://72.61.170.25:8000/chat`
  - Should return AI response

- [ ] **Test report generation** (the fixed endpoint)
  - Endpoint: `POST http://72.61.170.25:8000/generate_report`
  - Should NOT return 500 error anymore
  - If user has no conversation: Should return 404 with clear message

- [ ] **Monitor logs for errors**
  ```bash
  sudo journalctl -u fastapi -f
  ```
  Leave this running while testing

---

## ⚡ Enable Parallel Processing (4 Workers)

- [ ] **Find service file**
  ```bash
  sudo find /etc/systemd/system -name "*fastapi*"
  ```

- [ ] **Edit service file**
  ```bash
  sudo nano /etc/systemd/system/fastapi.service
  ```

- [ ] **Update ExecStart line**
  Change from:
  ```
  ExecStart=/usr/local/bin/gunicorn langraph_tool:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
  ```
  
  To:
  ```
  ExecStart=/usr/local/bin/gunicorn langraph_tool:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
  ```

- [ ] **Save and reload**
  ```bash
  # Save: Ctrl+O, Enter
  # Exit: Ctrl+X
  
  sudo systemctl daemon-reload
  sudo systemctl restart fastapi
  sudo systemctl status fastapi
  ```

- [ ] **Verify 4 workers are running**
  ```bash
  ps aux | grep gunicorn
  ```
  Should show 1 master + 4 worker processes

---

## 🐛 Troubleshooting

### Service won't start
```bash
# Check logs for errors
sudo journalctl -u fastapi -n 100 --no-pager

# Check for Python syntax errors
cd /root/app
python3 -m py_compile langraph_tool.py
```

### Still getting 500 errors
```bash
# Watch live logs while testing
sudo journalctl -u fastapi -f

# Trigger the endpoint and read the error
```

### Database connection issues
```bash
# Check environment variables
cd /root/app
cat .env | grep MONGO

# Test MongoDB connection
python3 << EOF
import os
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

async def test():
    uri = os.getenv('MONGO_DB_OFFICIAL')
    client = AsyncIOMotorClient(uri)
    await client.admin.command('ping')
    print("✓ MongoDB connected!")

asyncio.run(test())
EOF
```

---

## 📊 Performance Monitoring

- [ ] **Check CPU/Memory usage**
  ```bash
  htop
  ```

- [ ] **Check disk space**
  ```bash
  df -h
  ```

- [ ] **Monitor active connections**
  ```bash
  netstat -an | grep :8000
  ```

---

## 🎯 Success Criteria

✅ Service is running: `sudo systemctl status fastapi` shows "active (running)"
✅ Health endpoint responds: `curl http://72.61.170.25:8000/health` returns 200
✅ No errors in logs: `sudo journalctl -u fastapi -n 50` shows no exceptions
✅ Report generation works: No 500 errors, proper error messages for edge cases
✅ 4 workers running: `ps aux | grep gunicorn` shows 5 processes (1 master + 4 workers)

---

## 📝 Notes

- **Server IP**: 72.61.170.25
- **Default Port**: 8000
- **Service Name**: fastapi
- **App Directory**: /root/app (verify with `pwd` after SSH)
- **Log Command**: `sudo journalctl -u fastapi -f`

---

## 🔄 Future Deployments

For future code updates, just repeat:
1. Push to GitHub
2. SSH to VPS
3. `cd /root/app`
4. `git pull origin main`
5. `sudo systemctl restart fastapi`
6. Check logs: `sudo journalctl -u fastapi -n 20`

Or use the automated script: `./deploy_vps.sh`
