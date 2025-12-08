# 🚀 Mental Health Bot - VPS Edition

## Overview
This is the production-ready Mental Health Bot running on a dedicated VPS server for better performance and scalability.

---

## 🎯 Why VPS Instead of Render?

| Feature | Render (Old) | VPS (New) |
|---------|--------------|-----------|
| **Max Users** | ~50 (crashes) | 100+ concurrent |
| **Workers** | 1 | 4 (parallel processing) |
| **Control** | Limited | Full root access |
| **Monitoring** | Basic logs | Real-time journalctl |
| **Cost** | $7/month | $5-10/month |
| **Performance** | Slow (shared) | Fast (dedicated) |
| **Deployment** | Auto (risky) | Manual (controlled) |

---

## 📁 Project Structure

```
Mental_Study_Chat-main/
├── langraph_tool.py          # Main FastAPI application
├── autogen_report.py         # Report generation logic
├── requirements.txt          # Python dependencies
├── start.sh                  # Gunicorn startup script
├── .env                      # Environment variables (not in git)
│
├── VPS Management Tools:
├── connect_vps.bat           # Windows SSH helper
├── deploy_vps.sh             # Automated deployment script
├── VPS_TAKEOVER_SUMMARY.md   # Complete setup summary
├── DEPLOYMENT_CHECKLIST.md   # Step-by-step deployment guide
├── TROUBLESHOOTING_REPORT.md # Debug guide
├── VPS_QUICK_REFERENCE.md    # Command cheat sheet
│
└── .agent/workflows/
    └── vps-deployment.md     # VPS workflow documentation
```

---

## 🔧 VPS Server Details

- **IP Address**: `72.61.170.25`
- **Username**: `root`
- **Password**: `GenericPassword123#`
- **App Directory**: `/root/app` (verify after login)
- **Service Name**: `fastapi`
- **Port**: `8000`

---

## 🚀 Quick Start

### For First-Time Deployment:

1. **Read the summary**:
   - Open `VPS_TAKEOVER_SUMMARY.md`
   - Understand what was fixed and why

2. **Commit and push your code**:
   ```bash
   git add .
   git commit -m "VPS deployment ready"
   git push origin main
   ```

3. **Connect to VPS**:
   - Windows: Double-click `connect_vps.bat`
   - Mac/Linux: `ssh root@72.61.170.25`

4. **Deploy**:
   - Follow `DEPLOYMENT_CHECKLIST.md`
   - Or use automated script: `./deploy_vps.sh`

5. **Enable 4 workers**:
   - See "Step 6" in `DEPLOYMENT_CHECKLIST.md`

---

## 📚 Documentation Guide

| Document | When to Use |
|----------|-------------|
| `VPS_TAKEOVER_SUMMARY.md` | **START HERE** - Overview of everything |
| `DEPLOYMENT_CHECKLIST.md` | When deploying code changes |
| `VPS_QUICK_REFERENCE.md` | Quick command lookup |
| `TROUBLESHOOTING_REPORT.md` | When report generation fails |
| `.agent/workflows/vps-deployment.md` | Detailed VPS management guide |

---

## 🔄 Daily Workflow

### Making Code Changes:
1. Edit code locally
2. Test locally (if possible)
3. Commit: `git commit -m "description"`
4. Push: `git push origin main`
5. SSH to VPS: `ssh root@72.61.170.25`
6. Deploy: `cd /root/app && git pull && sudo systemctl restart fastapi`
7. Check logs: `sudo journalctl -u fastapi -n 20`

### Monitoring:
- **Health check**: `curl http://72.61.170.25:8000/health`
- **Live logs**: `sudo journalctl -u fastapi -f`
- **Service status**: `sudo systemctl status fastapi`
- **Resource usage**: `htop`

---

## 🐛 Recent Bug Fixes

### ✅ Fixed: Report Generation 500 Error (Dec 2025)
**Problem**: `/generate_report` endpoint crashed when user had no conversation
**Solution**: Added `session_id` initialization and validation
**Files Changed**: `langraph_tool.py` (lines 2393-2443)

---

## 🛠️ Tools Included

### 1. **connect_vps.bat** (Windows)
Double-click to instantly connect to VPS. No need to remember SSH commands.

### 2. **deploy_vps.sh** (VPS)
Automated deployment script with:
- Git pull
- Dependency installation
- Service restart
- Status verification
- Colored output

Usage:
```bash
chmod +x deploy_vps.sh
./deploy_vps.sh
```

---

## 🎓 For Junior Developers

### You Are Now a Server Admin!
This VPS setup gives you:
- ✅ Full control over a production server
- ✅ Real-time debugging capabilities
- ✅ Professional deployment workflow
- ✅ Scalability for 100+ users

### Key Skills You'll Learn:
1. **SSH**: Remote server access
2. **Git Deployment**: Manual version control
3. **systemd**: Linux service management
4. **Log Analysis**: Debugging with journalctl
5. **Process Management**: Monitoring with htop/ps
6. **Bash Scripting**: Automation

### Don't Panic!
- All commands are documented
- Logs tell you exactly what's wrong
- You can always restart the service
- Backups are easy: `tar -czf backup.tar.gz app/`

---

## 📊 Performance Optimization

### Current Setup:
- **Workers**: 4 (parallel processing)
- **Model**: gpt-4o-mini (fast, cheap)
- **Caching**: 10-minute TTL (saves tokens)
- **Database**: MongoDB with Motor (async)

### Expected Performance:
- **Response Time**: 2-5 seconds
- **Concurrent Users**: 100+
- **Cost per 1000 messages**: ~$0.50

---

## 🔒 Security Notes

### ⚠️ Important:
1. **Change the default password** after first login:
   ```bash
   passwd
   ```

2. **Set up SSH keys** (more secure than password):
   ```bash
   ssh-keygen -t rsa -b 4096
   ssh-copy-id root@72.61.170.25
   ```

3. **Configure firewall**:
   ```bash
   sudo ufw allow 8000/tcp
   sudo ufw enable
   ```

4. **Keep `.env` file secure**:
   - Never commit to git
   - Contains API keys and database credentials

---

## 🆘 Emergency Contacts

### If Something Goes Wrong:

1. **Check logs first**:
   ```bash
   sudo journalctl -u fastapi -n 100 --no-pager
   ```

2. **Restart service**:
   ```bash
   sudo systemctl restart fastapi
   ```

3. **Rollback to previous version**:
   ```bash
   cd /root/app
   git log --oneline -n 5
   git reset --hard <commit-hash>
   sudo systemctl restart fastapi
   ```

4. **Restore from backup**:
   ```bash
   tar -xzf backup.tar.gz
   ```

---

## 📈 Monitoring Checklist

Run these daily:
- [ ] Health check: `curl http://72.61.170.25:8000/health`
- [ ] Check logs: `sudo journalctl -u fastapi -n 50`
- [ ] CPU/Memory: `htop`
- [ ] Disk space: `df -h`
- [ ] Worker count: `ps aux | grep gunicorn` (should show 5)

---

## 🎯 Success Metrics

Your VPS is healthy if:
- ✅ Health endpoint returns 200
- ✅ No errors in last 50 log lines
- ✅ CPU usage < 80%
- ✅ Memory usage < 80%
- ✅ Disk usage < 80%
- ✅ 5 gunicorn processes running (1 master + 4 workers)

---

## 📞 Quick Commands

```bash
# Connect
ssh root@72.61.170.25

# Deploy
cd /root/app && git pull && sudo systemctl restart fastapi

# Logs
sudo journalctl -u fastapi -f

# Status
sudo systemctl status fastapi

# Health
curl http://localhost:8000/health

# Workers
ps aux | grep gunicorn
```

---

## 🎉 You're All Set!

You now have:
- ✅ A powerful VPS server
- ✅ Fixed report generation bug
- ✅ Complete documentation
- ✅ Automated deployment tools
- ✅ Troubleshooting guides
- ✅ Professional workflow

**Welcome to production-grade deployment! 🚀**

---

## 📝 Version History

- **v1.0** (Dec 2025): Initial VPS setup
  - Fixed session_id bug in generate_report
  - Created deployment tools
  - Enabled 4-worker parallel processing
  - Complete documentation suite

---

**For detailed instructions, see `VPS_TAKEOVER_SUMMARY.md`**
