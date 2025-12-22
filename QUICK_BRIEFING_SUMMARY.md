# 🚀 Quick Briefing Summary - Mental Health Bot VPS Backend

**For:** New Team Lead  
**Date:** December 22, 2025

---

## 🎯 What We Built

A **production-grade Mental Health Chatbot** running on a VPS server, handling **100+ concurrent users** with AI-powered conversation, exam coaching, and mental health reporting.

---

## 🖥️ The Server

```
IP: 72.61.170.25
Login: ssh root@72.61.170.25
Password: GenericPassword123#
App Location: /root/app
```

---

## 🏗️ What's Inside

### **Main Application** (`langraph_tool.py` - 2,715 lines)
- FastAPI backend with 4 parallel workers
- LangGraph AI orchestration
- MongoDB async database
- OpenAI GPT-4o-mini integration

### **Key Features**
1. **Mental Health Chatbot** - Emotion detection + intelligent routing
2. **Exam Buddy** - JEE/NEET study coaching
3. **Report Generator** - Mental health assessments
4. **Analytics** - Real-time user tracking

---

## 📊 Performance

| Metric | Before (Render) | After (VPS) |
|--------|----------------|-------------|
| Max Users | 50 (crashes) | 100+ |
| Workers | 1 | 4 |
| Response Time | 5-10s | 2-5s |
| Control | Limited | Full |
| Cost | $7/mo | $5-10/mo |

---

## 🔧 Tech Stack

```
Frontend → FastAPI → LangGraph → OpenAI GPT-4o-mini
                  ↓
              MongoDB (async)
                  ↓
         Gunicorn (4 workers)
                  ↓
         systemd (service manager)
```

---

## 🚀 How to Deploy

```bash
# 1. Local: Push code
git push origin main

# 2. VPS: Connect
ssh root@72.61.170.25

# 3. VPS: Deploy
cd /root/app
git pull origin main
sudo systemctl restart fastapi

# 4. VPS: Verify
sudo journalctl -u fastapi -n 20
curl http://localhost:8000/health
```

**Or use automated script:** `./deploy_vps.sh`

---

## 📈 Essential Commands

```bash
# Live logs (most important!)
sudo journalctl -u fastapi -f

# Service status
sudo systemctl status fastapi

# Health check
curl http://72.61.170.25:8000/health

# Active users
curl http://72.61.170.25:8000/analytics/active_users

# Worker count (should be 5)
ps aux | grep gunicorn

# System resources
htop
```

---

## 🐛 Recent Fix (Dec 2025)

**Problem:** `/generate_report` crashed with 500 error  
**Cause:** `session_id` undefined when user had no chat history  
**Fix:** Initialize variables + add validation  
**Status:** ✅ Fixed and deployed

---

## 📚 Documentation

| File | Use Case |
|------|----------|
| `TEAM_LEAD_BRIEFING.md` | **Full briefing (read this!)** |
| `README_VPS.md` | VPS overview |
| `DEPLOYMENT_CHECKLIST.md` | Deployment steps |
| `VPS_QUICK_REFERENCE.md` | Command cheat sheet |
| `TROUBLESHOOTING_REPORT.md` | Debug guide |

---

## 🔐 Important Files

### **Never Commit to Git:**
- `.env` - Contains API keys and database credentials

### **Key Environment Variables:**
```
OPENAI_API_KEY=sk-...
HF_TOKEN=hf_...
MONGO_DB_OFFICIAL=mongodb+srv://...
MONGO_DB_NAME_OFFICIAL=zenark_db
PORT=8000
```

---

## ✅ Health Checklist

Your system is healthy if:
- ✅ `curl http://72.61.170.25:8000/health` returns 200
- ✅ `sudo systemctl status fastapi` shows "active (running)"
- ✅ `ps aux | grep gunicorn` shows 5 processes (1 master + 4 workers)
- ✅ No errors in last 50 log lines
- ✅ CPU < 80%, Memory < 80%

---

## 🆘 Quick Troubleshooting

### Service won't start?
```bash
sudo journalctl -u fastapi -n 100 --no-pager
```

### 500 errors?
```bash
sudo journalctl -u fastapi -f
# Then trigger the endpoint and watch
```

### Need to rollback?
```bash
cd /root/app
git log --oneline -n 5
git reset --hard <commit-hash>
sudo systemctl restart fastapi
```

---

## 🎯 Your First Week

### Day 1-2: Explore
- [ ] SSH into VPS
- [ ] Navigate around `/root/app`
- [ ] Read `TEAM_LEAD_BRIEFING.md`
- [ ] Watch logs: `sudo journalctl -u fastapi -f`

### Day 3-4: Test
- [ ] Make a small code change locally
- [ ] Deploy to VPS
- [ ] Verify it works
- [ ] Check logs for errors

### Day 5: Monitor
- [ ] Check health endpoint
- [ ] Review analytics
- [ ] Monitor CPU/memory
- [ ] Understand worker processes

---

## 💡 Pro Tips

1. **Logs are your best friend** - Always check them first
2. **Test locally** - Before deploying to VPS
3. **Use automated deployment** - `./deploy_vps.sh`
4. **Monitor daily** - Health endpoint + logs
5. **Backup before changes** - `tar -czf backup.tar.gz app/`

---

## 📞 Key Endpoints

```
Health:        GET  /health
Chat:          POST /chat
Exam Buddy:    POST /exam_buddy
Report:        POST /generate_report
Active Users:  GET  /analytics/active_users
Dashboard:     GET  /analytics/dashboard
```

---

## 🎉 Bottom Line

You're managing a **professional-grade AI backend** that:
- Handles 100+ users simultaneously
- Uses cutting-edge AI orchestration
- Has comprehensive monitoring
- Is production-ready and stable
- Costs less than a Netflix subscription

**Welcome to the team! 🚀**

---

## 📖 Next Steps

1. Read `TEAM_LEAD_BRIEFING.md` (full details)
2. SSH into VPS and explore
3. Test the deployment process
4. Set up monitoring alerts
5. Plan security improvements

---

*For detailed information, see `TEAM_LEAD_BRIEFING.md`*  
*Last Updated: December 22, 2025*
