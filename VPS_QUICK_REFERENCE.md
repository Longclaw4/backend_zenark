# 📋 VPS Quick Reference Card

## 🔐 Connection
```bash
ssh root@72.61.170.25
# Password: GenericPassword123#
```

---

## 🚀 Deployment (Quick)
```bash
cd /root/app
git pull origin main
sudo systemctl restart fastapi
sudo systemctl status fastapi
```

---

## 📊 Monitoring

### View Live Logs
```bash
sudo journalctl -u fastapi -f
```
Press `Ctrl+C` to stop

### View Last 50 Lines
```bash
sudo journalctl -u fastapi -n 50 --no-pager
```

### View Only Errors
```bash
sudo journalctl -u fastapi -n 100 | grep -i error
```

---

## 🔧 Service Control

### Check Status
```bash
sudo systemctl status fastapi
```

### Restart Service
```bash
sudo systemctl restart fastapi
```

### Stop Service
```bash
sudo systemctl stop fastapi
```

### Start Service
```bash
sudo systemctl start fastapi
```

### Enable Auto-Start on Boot
```bash
sudo systemctl enable fastapi
```

---

## 🐛 Debugging

### Test Python Syntax
```bash
cd /root/app
python3 -m py_compile langraph_tool.py
```

### Check Environment Variables
```bash
cd /root/app
cat .env
```

### Test MongoDB Connection
```bash
cd /root/app
python3 -c "from pymongo import MongoClient; import os; client = MongoClient(os.getenv('MONGO_DB_OFFICIAL')); print(client.server_info())"
```

### Check Running Processes
```bash
ps aux | grep gunicorn
```

### Check Port Usage
```bash
sudo lsof -i :8000
```

### Kill Process by PID
```bash
sudo kill -9 <PID>
```

---

## 📈 Performance

### CPU & Memory Usage
```bash
htop
# Press 'q' to quit
```

### Disk Space
```bash
df -h
```

### Network Connections
```bash
netstat -an | grep :8000
```

---

## 📝 File Operations

### View File
```bash
cat filename.py
# OR
nano filename.py  # Press Ctrl+X to exit
```

### Edit File
```bash
nano filename.py
# Save: Ctrl+O, Enter
# Exit: Ctrl+X
```

### Find Files
```bash
find /root -name "*.py"
```

### Check Git Status
```bash
cd /root/app
git status
git log -n 5  # Last 5 commits
```

---

## 🔄 Service Configuration

### View Service File
```bash
sudo systemctl cat fastapi
```

### Edit Service File
```bash
sudo nano /etc/systemd/system/fastapi.service
```

### Reload After Editing
```bash
sudo systemctl daemon-reload
sudo systemctl restart fastapi
```

---

## 🧪 Testing

### Health Check
```bash
curl http://localhost:8000/health
# OR
curl http://72.61.170.25:8000/health
```

### Test Endpoint with POST
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"test","session_id":"test123","token":"YOUR_TOKEN"}'
```

---

## 🔒 Security

### Change Root Password
```bash
passwd
```

### View Failed Login Attempts
```bash
sudo journalctl -u ssh -n 50 | grep -i failed
```

### Check Firewall Status
```bash
sudo ufw status
```

---

## 💾 Backup

### Backup App Directory
```bash
cd /root
tar -czf app_backup_$(date +%Y%m%d_%H%M%S).tar.gz app/
```

### List Backups
```bash
ls -lh /root/*.tar.gz
```

### Restore from Backup
```bash
tar -xzf app_backup_YYYYMMDD_HHMMSS.tar.gz
```

---

## 🆘 Emergency Commands

### Restart Entire Server
```bash
sudo reboot
```

### View System Logs
```bash
sudo journalctl -xe
```

### Check System Resources
```bash
free -h  # Memory
df -h    # Disk
uptime   # Uptime and load
```

---

## 📞 Quick Help

| Problem | Command |
|---------|---------|
| Service won't start | `sudo journalctl -u fastapi -n 100` |
| High CPU usage | `htop` |
| Port already in use | `sudo lsof -i :8000` |
| Git conflicts | `git stash && git pull` |
| Syntax error | `python3 -m py_compile langraph_tool.py` |
| Database error | Check `.env` file |
| Out of disk space | `df -h` then clean logs |

---

## 🎯 Most Used Commands (Top 5)

1. **Deploy**: `cd /root/app && git pull && sudo systemctl restart fastapi`
2. **Logs**: `sudo journalctl -u fastapi -f`
3. **Status**: `sudo systemctl status fastapi`
4. **Health**: `curl http://localhost:8000/health`
5. **Processes**: `ps aux | grep gunicorn`

---

**Print this and keep it handy! 📌**
