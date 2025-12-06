# 🚀 Zenark Backend - Render Deployment Guide

## ✅ What I've Created

All necessary files for deploying your FastAPI backend to Render:

### 📦 Configuration Files
- **`requirements.txt`** - Python dependencies
- **`start.sh`** - Startup script for Render
- **`render.yaml`** - Render blueprint (optional)
- **`.gitignore`** - Git ignore rules

### 🔧 Placeholder Files (Replace with your actual implementations)
- **`Guideliness.py`** - Action scoring guidelines
- **`autogen_report.py`** - Report generation logic
- **`api_key_rotator.py`** - API key rotation
- **`exam_buddy.py`** - Exam buddy responses

### 📊 Dataset Files (Minimal versions - replace with your full datasets)
- **`positive_conversation.json`** - Positive conversation templates
- **`combined_dataset.json`** - Negative emotion templates
- **`dataset/combined_intents_empathic.json`** - Empathic intent patterns
- **`dataset/Intent.json`** - General intent patterns

---

## 🌐 Deployment Steps

### 1. **Prepare Your Repository**
```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Zenark backend"

# Push to GitHub/GitLab
git remote add origin YOUR_REPO_URL
git push -u origin main
```

### 2. **Create Render Web Service**
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub/GitLab repository
4. Configure:
   - **Name**: `zenark-backend` (or your choice)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `./start.sh`
   - **Instance Type**: Free or Starter (upgrade as needed)

### 3. **Set Environment Variables**
In Render dashboard, add these environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | `sk-...` |
| `HF_TOKEN` | Hugging Face token | `hf_...` |
| `MONGO_DB_OFFICIAL` | MongoDB connection string | `mongodb+srv://...` |
| `MONGO_DB_NAME_OFFICIAL` | Database name | `zenark_db` |

### 4. **Deploy**
- Click **"Create Web Service"**
- Render will automatically build and deploy
- Wait for deployment to complete (~5-10 minutes)

### 5. **Get Your API URL**
Once deployed, Render provides a URL like:
```
https://zenark-backend.onrender.com
```

**Give this URL to your frontend engineer!**

---

## 🔗 API Endpoints

Your backend exposes these endpoints (based on the code):

### Chat Endpoint
```
POST https://YOUR_RENDER_URL/chat
```

### Report Generation
```
POST https://YOUR_RENDER_URL/generate-report
```

### Health Check
```
GET https://YOUR_RENDER_URL/
```

---

## ⚠️ Important Notes

### 1. **Replace Placeholder Files**
The following files are **minimal placeholders**. Replace them with your actual implementations:
- `Guideliness.py`
- `autogen_report.py`
- `api_key_rotator.py`
- `exam_buddy.py`
- All JSON dataset files

### 2. **Cold Start Warning**
Render's free tier has **cold starts** (app sleeps after 15 min of inactivity). First request after sleep takes ~30-60 seconds. Upgrade to paid tier to avoid this.

### 3. **MongoDB Atlas**
Ensure your MongoDB Atlas cluster:
- Allows connections from **0.0.0.0/0** (or Render's IP ranges)
- Has proper authentication configured

### 4. **Logs & Debugging**
View logs in Render dashboard:
- Go to your service → **"Logs"** tab
- Check for startup errors

---

## 🧪 Testing Your Deployment

### Test with curl:
```bash
curl -X POST https://YOUR_RENDER_URL/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, I need help",
    "session_id": "test-session-123"
  }'
```

### Test in browser:
Visit `https://YOUR_RENDER_URL/docs` for interactive API documentation (FastAPI auto-generates this).

---

## 📞 For Your Frontend Engineer

Share this information:

**Base URL**: `https://YOUR_RENDER_URL`

**Example Request**:
```javascript
const response = await fetch('https://YOUR_RENDER_URL/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'I am feeling stressed about exams',
    session_id: 'user-session-id-here'
  })
});

const data = await response.json();
console.log(data);
```

---

## 🐛 Troubleshooting

### Build fails?
- Check `requirements.txt` for typos
- Ensure all imported modules exist
- Check Render logs for specific errors

### App crashes on startup?
- Verify environment variables are set correctly
- Check MongoDB connection string
- Review startup logs in Render dashboard

### Slow responses?
- Free tier has limited resources
- Consider upgrading to paid tier
- Check MongoDB query performance

---

## 📈 Next Steps

1. ✅ Replace placeholder files with actual implementations
2. ✅ Test all endpoints thoroughly
3. ✅ Monitor logs for errors
4. ✅ Set up proper error tracking (e.g., Sentry)
5. ✅ Configure CORS if needed for frontend
6. ✅ Consider upgrading Render tier for production

---

**Need help?** Check Render's [documentation](https://render.com/docs) or their support.
