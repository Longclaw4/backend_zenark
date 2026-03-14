# 🧠 Zenark: Mental Health & Academic Assistant

Zenark is an AI-powered platform designed to support students' mental well-being and academic performance. It combines an empathic mental health chatbot with a powerful academic assistant and a data-driven dashboard for educators.

## 📂 Project Structure

- **`/Heatblast`**: FastAPI Backend (Mental health AI, Academic assistant, Data Proxy).
- **`/xylene_v2`**: React Native (Expo) Frontend - Modern dashboard and mobile app.

---

## 🚀 Backend Setup (Heatblast)

The backend handles AI logic, database interactions, and proxies academic data.

### 1. Prerequisites
- Python 3.10+
- MongoDB Atlas account

### 2. Installation
```bash
cd Heatblast
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the `Heatblast` directory:
```env
OPENAI_API_KEY=sk-...
MONGO_DB_OFFICIAL=mongodb+srv://...
MONGO_DB_NAME_OFFICIAL=zenark_db
GHOSTFREAK_BASE_URL=https://ghostfreak-production.up.railway.app
```

### 4. Running Locally
```bash
python app.py
# or
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

---

## 📱 Frontend Setup (xylene_v2)

The frontend is a cross-platform React Native app powered by Expo.

### 1. Installation
```bash
cd xylene_v2
npm install
```

### 2. Running
```bash
# Web
npm run web

# Mobile (requires Expo Go app)
npx expo start
```

### 3. API Configuration
Open `App.js` or your config file and ensure the `API_BASE_URL` points to your running backend (e.g., `http://localhost:8000`).

---

## 🛠️ Key Features

- **Mental Health Chat**: Context-aware AI using LangGraph for empathic conversations.
- **Academic Assistant**: Specialized support for academic queries and exam preparation.
- **Unified Dashboard**: Real-time analytics for teachers, including:
    - Academic Health Index (AHI).
    - Mental Wellness Trends.
    - Class Strengths & Weaknesses (Proxied from Ghostfreak).
    - Student Well-being Monitoring.
- **Zen Mode**: Focus-enhancing features for students.

---

## ☁️ Deployment

### Backend (Railway)
1. Push your changes to GitHub.
2. Connect your repo to [Railway](https://railway.app).
3. Ensure the following variables are set in Railway:
    - `MONGO_DB_OFFICIAL`
    - `OPENAI_API_KEY`
4. The repo includes a `Procfile` for automatic startup.

### Frontend
The frontend can be built for web or deployed via Expo EAS for mobile.

---

## 🤝 Contributing
For updates to the dashboard or data structures, please refer to the `walkthrough.md` in the project brain or `Heatblast/api_contract_report.md`.
