# Quick Fix Guide - Chatbot Connection Error

## 🎯 Problem Summary

Your chatbot shows: **"I'm having trouble connecting to the AI service"**

**Root Cause:** The Qdrant vector database is empty because the Gemini API quota has been exceeded.

---

## ✅ Quick Solution (When Quota Resets)

Run this single command:

```bash
cd backend
python check_and_ingest.py
```

This script will:
1. ✅ Check if your API quota has reset
2. ✅ Automatically run ingestion if quota is available
3. ✅ Populate the database with sample content
4. ✅ Make your chatbot functional

**Time:** ~30 seconds once quota is available

---

## 📅 When Will Quota Reset?

- **Free tier quota resets:** Every 24 hours (midnight UTC)
- **Check your usage:** https://ai.dev/usage?tab=rate-limit

---

## 🚀 Alternative: Use a New API Key (Immediate Fix)

If you have another Google account:

1. **Get a new API key:**
   - Visit: https://aistudio.google.com/app/apikey
   - Create a new key

2. **Update your .env file:**
   ```bash
   # Edit backend/.env or root .env
   GEMINI_API_KEY=your_new_api_key_here
   ```

3. **Run ingestion:**
   ```bash
   cd backend
   python check_and_ingest.py
   ```

---

## 🧪 Verify It's Working

After ingestion completes:

1. **Check database has data:**
   ```bash
   cd backend
   python check_qdrant.py
   ```
   Should show: `Points count: 5` (or more)

2. **Test the chatbot:**
   - Open your website
   - Click the "🤖 Ask AI" button
   - Ask: "What is ROS 2?"
   - You should get a detailed response!

---

## 📊 Current Status

| Component | Status |
|-----------|--------|
| Backend Server | ✅ Running on port 8000 |
| Qdrant Database | ✅ Connected (but empty) |
| Gemini API | ❌ Quota exceeded |
| **Action Needed** | **Wait for quota reset OR use new API key** |

---

## 🆘 Still Not Working?

1. **Make sure backend is running:**
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Check if you can access the health endpoint:**
   ```bash
   curl http://127.0.0.1:8000/health
   ```
   Should return: `{"status":"ok"}`

3. **Review the full diagnosis:**
   See `CHATBOT_ERROR_DIAGNOSIS.md` for detailed troubleshooting

---

## 💡 Pro Tips

- **For testing:** Use `quick_ingest.py` (5 sample docs, fast)
- **For production:** Use `ingest.py` (all 19 docs, comprehensive)
- **Monitor quota:** Check https://ai.dev/usage regularly
- **Upgrade plan:** Consider paid tier if you need higher limits

---

**Need help?** Check the full diagnosis in `CHATBOT_ERROR_DIAGNOSIS.md`
