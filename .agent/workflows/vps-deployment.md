---
description: Deploy and manage the Mental Health Bot on VPS (72.61.170.25)
---

# VPS Deployment Workflow

## Prerequisites
- VPS Server: `72.61.170.25`
- Username: `root`
- Password: `GenericPassword123#`
- GitHub repo must be pushed with latest changes

---

## Step 1: Initial SSH Connection
```bash
ssh root@72.61.170.25
```
Enter password when prompted: `GenericPassword123#`

---

## Step 2: Locate the Application Directory
Once logged in, find where the app is located:
```bash
# List all directories
ls -la

# Common locations to check:
cd /root/app || cd /root/backend || cd /root/fastapi || cd /opt/app
pwd  # Print current directory to confirm location
```

**Note the path** - you'll need it for all future deployments.

---

## Step 3: Deploy New Code (After Git Push)

### 3a. Navigate to app directory
```bash
cd /root/app  # Replace with actual path from Step 2
```

### 3b. Pull latest changes
```bash
git pull origin main
```

### 3c. Install/Update dependencies (if requirements.txt changed)
```bash
pip install -r requirements.txt
```

### 3d. Restart the FastAPI service
```bash
sudo systemctl restart fastapi
```

### 3e. Verify service is running
```bash
sudo systemctl status fastapi
```

---

## Step 4: View Live Logs (For Debugging)

### View real-time logs
```bash
sudo journalctl -u fastapi -f
```
Press `Ctrl+C` to stop viewing logs.

### View last 100 lines of logs
```bash
sudo journalctl -u fastapi -n 100
```

### View logs with timestamps
```bash
sudo journalctl -u fastapi -n 50 --no-pager
```

---

## Step 5: Fix Report Generation Crash

### 5a. Check current logs for errors
```bash
sudo journalctl -u fastapi -n 200 | grep -i error
```

### 5b. Test the endpoint and watch logs
In one terminal window:
```bash
sudo journalctl -u fastapi -f
```

In another terminal/Postman, trigger the `/generate_report` endpoint.

### 5c. Common issues to check:
1. **Database connection**: Verify MongoDB URI in environment variables
2. **Missing collections**: Ensure `chats` and `reports` collections exist
3. **API key issues**: Check OpenAI API key is valid and has credits
4. **Memory issues**: Check if server has enough RAM

---

## Step 6: Enable Parallel Processing (4 Workers)

### 6a. Find the systemd service file
```bash
sudo find /etc/systemd/system -name "*fastapi*"
# OR
ls -la /etc/systemd/system/ | grep fastapi
```

### 6b. Edit the service file
```bash
sudo nano /etc/systemd/system/fastapi.service
```

### 6c. Modify the ExecStart line
Find the line starting with `ExecStart=` and ensure it has `-w 4`:

**Before:**
```
ExecStart=/usr/local/bin/gunicorn langraph_tool:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**After:**
```
ExecStart=/usr/local/bin/gunicorn langraph_tool:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 6d. Save and exit
- Press `Ctrl+O` to save
- Press `Enter` to confirm
- Press `Ctrl+X` to exit

### 6e. Reload systemd and restart service
```bash
sudo systemctl daemon-reload
sudo systemctl restart fastapi
sudo systemctl status fastapi
```

---

## Step 7: Monitor Server Resources

### Check CPU and Memory usage
```bash
htop
# OR
top
```
Press `q` to quit.

### Check disk space
```bash
df -h
```

### Check running processes
```bash
ps aux | grep gunicorn
```

---

## Step 8: Environment Variables Check

### View current environment variables
```bash
# If using .env file
cat /root/app/.env

# If using systemd environment file
cat /etc/systemd/system/fastapi.service
```

### Required environment variables:
- `OPENAI_API_KEY`
- `HF_TOKEN`
- `MONGO_DB_OFFICIAL`
- `MONGO_DB_NAME_OFFICIAL`
- `PORT` (usually 8000)

---

## Step 9: Backup and Rollback

### Create a backup before major changes
```bash
cd /root
tar -czf app_backup_$(date +%Y%m%d_%H%M%S).tar.gz app/
```

### Rollback to previous commit (if deployment fails)
```bash
cd /root/app
git log --oneline -n 5  # See recent commits
git reset --hard <commit-hash>  # Replace with actual hash
sudo systemctl restart fastapi
```

---

## Step 10: Quick Health Check

### Test if API is responding
```bash
curl http://localhost:8000/health
# OR
curl http://72.61.170.25:8000/health
```

---

## Common Commands Cheat Sheet

| Task | Command |
|------|---------|
| SSH into server | `ssh root@72.61.170.25` |
| Navigate to app | `cd /root/app` |
| Pull latest code | `git pull origin main` |
| Restart service | `sudo systemctl restart fastapi` |
| View logs | `sudo journalctl -u fastapi -f` |
| Check status | `sudo systemctl status fastapi` |
| Stop service | `sudo systemctl stop fastapi` |
| Start service | `sudo systemctl start fastapi` |
| Edit service file | `sudo nano /etc/systemd/system/fastapi.service` |
| Reload systemd | `sudo systemctl daemon-reload` |

---

## Troubleshooting

### Service won't start
```bash
# Check for syntax errors in code
cd /root/app
python3 -m py_compile langraph_tool.py

# Check service logs
sudo journalctl -u fastapi -n 100 --no-pager
```

### Port already in use
```bash
# Find process using port 8000
sudo lsof -i :8000

# Kill the process (replace PID)
sudo kill -9 <PID>
```

### Database connection issues
```bash
# Test MongoDB connection
python3 -c "from pymongo import MongoClient; client = MongoClient('YOUR_MONGO_URI'); print(client.server_info())"
```

---

## Security Notes
1. **Change default password** after first login
2. **Set up SSH keys** instead of password authentication
3. **Configure firewall** to only allow necessary ports
4. **Regular backups** of database and code
5. **Monitor logs** for suspicious activity
