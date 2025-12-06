# 🚀 How to Run the Project

## ✅ Frontend is Already Running!

Your Docusaurus frontend is running at: **http://localhost:3000**

Open your browser and visit the site to see:
- Course homepage
- Navigation sidebar
- Chat widget (bottom-right corner)
- All course content

---

## 🔧 To Run the Backend

### Quick Start (Windows)

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Set up environment variables**:
   ```bash
   copy .env.example .env
   ```
   
   Then edit `.env` file and add your API keys:
   - `GEMINI_API_KEY` - Get from https://ai.google.dev
   - `QDRANT_URL` - Get from https://cloud.qdrant.io
   - `QDRANT_API_KEY` - Get from https://cloud.qdrant.io
   - `DATABASE_URL` - Get from https://neon.tech

3. **Run the backend**:
   ```bash
   start.bat
   ```
   
   This will:
   - Create virtual environment (if needed)
   - Install dependencies (if needed)
   - Start the FastAPI server

4. **Backend will be available at**:
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs

### Manual Start (Alternative)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload
```

---

## 📚 To Ingest Content

After backend is running, ingest the textbook content:

### Quick Start
```bash
cd backend
ingest.bat
```

### Manual
```bash
cd backend
venv\Scripts\activate
python scripts\ingest_content.py
```

This will populate your Qdrant database with the course content.

---

## 🧪 Testing the Complete System

1. **Frontend**: http://localhost:3000 ✅ (Already running!)
2. **Backend**: http://localhost:8000 (Start with `start.bat`)
3. **Test Chatbot**:
   - Click chat button (bottom-right)
   - Ask: "What is ROS 2?"
   - You should get an AI-powered answer!

---

## 📁 Project URLs

| Service | URL | Status |
|---------|-----|--------|
| Frontend | http://localhost:3000 | ✅ Running |
| Backend API | http://localhost:8000 | ⏳ Ready to start |
| API Docs | http://localhost:8000/docs | ⏳ Ready to start |
| Health Check | http://localhost:8000/health | ⏳ Ready to start |

---

## 🔑 Getting API Keys (Free!)

### 1. Google Gemini API
1. Visit https://ai.google.dev
2. Click "Get API Key"
3. Create a new API key
4. Copy to `.env` file

### 2. Qdrant Cloud
1. Visit https://cloud.qdrant.io
2. Sign up for free
3. Create a cluster
4. Copy URL and API key to `.env`

### 3. Neon Postgres
1. Visit https://neon.tech
2. Sign up for free
3. Create a project
4. Copy connection string to `.env`

---

## 🐛 Troubleshooting

### Port 3000 Already in Use
✅ This is fine! It means the frontend is already running.

### Backend Won't Start
- Check `.env` file exists and has valid API keys
- Make sure Python 3.11+ is installed
- Try running `pip install -r requirements.txt` manually

### Chatbot Not Responding
1. Make sure backend is running
2. Check backend logs for errors
3. Verify content is ingested
4. Check browser console (F12)

### CORS Errors
- Make sure `CORS_ORIGINS` in `.env` includes `http://localhost:3000`

---

## 📊 What Each Component Does

### Frontend (Port 3000)
- Serves the Docusaurus website
- Displays course content
- Provides chat widget UI
- Handles user interactions

### Backend (Port 8000)
- Processes chat queries
- Performs RAG (Retrieval-Augmented Generation)
- Connects to Gemini API
- Manages Qdrant vector search
- Handles personalization & translation

### Qdrant (Cloud)
- Stores content embeddings
- Performs vector similarity search
- Returns relevant content chunks

### Neon Postgres (Cloud)
- Stores user data
- Caches translations
- Stores chat history

---

## ✨ Features to Test

1. **Chat**: Click chat button, ask questions
2. **Text Selection**: Highlight text, click "Ask AI"
3. **Navigation**: Browse through modules
4. **Dark Mode**: Toggle in top-right
5. **Mobile**: Resize browser window

---

## 🚀 Next Steps

1. ✅ Frontend running
2. ⏳ Start backend (`cd backend && start.bat`)
3. ⏳ Ingest content (`cd backend && ingest.bat`)
4. ⏳ Test chatbot
5. ⏳ Deploy to Netlify/Railway
6. ⏳ Create demo video
7. ⏳ Submit to hackathon!

---

## 💡 Quick Commands

```bash
# Start frontend (if not running)
cd frontend
npm start

# Start backend
cd backend
start.bat

# Ingest content
cd backend
ingest.bat

# View backend logs
# Check the terminal where backend is running
```

---

## 🎯 You're Almost There!

The frontend is running beautifully! Just:
1. Get your API keys (free!)
2. Run `start.bat` in backend folder
3. Run `ingest.bat` to load content
4. Test the chatbot
5. You're ready to deploy!

**Need help?** Check the other documentation files or use the chatbot once it's running!

---

Built with ❤️ for the Panaversity Hackathon
