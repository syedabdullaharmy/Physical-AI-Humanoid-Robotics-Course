# ⚡ QUICK START - Physical AI Textbook

## ✅ Frontend is Already Running!

Your frontend is **LIVE** at: **http://localhost:3000**

Just open your browser and visit that URL!

---

## 🎯 Three Ways to Start the Project

### Option 1: Frontend Only (Already Running!)
```bash
# From root directory
start-frontend.bat

# OR from frontend directory
cd frontend
npm start
```

### Option 2: Backend Only
```bash
# From root directory
cd backend
start.bat
```

### Option 3: Start Everything
```bash
# From root directory
start-all.bat
```

---

## ⚠️ Common Mistake

**DON'T** run `npm start` from the root directory!

❌ **Wrong**:
```bash
C:\Users\FA.COM\Pictures\Camera Roll\doker> npm start
```

✅ **Correct**:
```bash
C:\Users\FA.COM\Pictures\Camera Roll\doker> cd frontend
C:\Users\FA.COM\Pictures\Camera Roll\doker\frontend> npm start
```

**OR** use the provided scripts:
```bash
C:\Users\FA.COM\Pictures\Camera Roll\doker> start-frontend.bat
```

---

## 📁 Project Structure

```
doker/
├── start-frontend.bat    ← Start frontend from root
├── start-all.bat         ← Start both servers
├── frontend/             ← Frontend code
│   └── npm start here!
└── backend/              ← Backend code
    ├── start.bat         ← Start backend
    └── ingest.bat        ← Load content
```

---

## 🚀 What's Running Now

| Service | Status | URL |
|---------|--------|-----|
| Frontend | ✅ RUNNING | http://localhost:3000 |
| Backend | ⏳ Not started | http://localhost:8000 |

---

## 🔧 To Start Backend

1. **Get API keys** (free):
   - Gemini: https://ai.google.dev
   - Qdrant: https://cloud.qdrant.io
   - Neon: https://neon.tech

2. **Configure**:
   ```bash
   cd backend
   copy .env.example .env
   # Edit .env with your API keys
   ```

3. **Start**:
   ```bash
   start.bat
   ```

4. **Load content**:
   ```bash
   ingest.bat
   ```

---

## ✨ Test the Frontend Now!

1. Open http://localhost:3000
2. Browse the course content
3. Check out the navigation
4. See the chat widget (bottom-right)
   - Note: Chat won't work until backend is running

---

## 📖 Full Documentation

- **HOW_TO_RUN.md** - Complete running guide
- **START_HERE.md** - Project overview
- **DEPLOYMENT.md** - Deploy to production

---

**You're all set!** Frontend is running. Just start the backend when you have your API keys! 🎉
