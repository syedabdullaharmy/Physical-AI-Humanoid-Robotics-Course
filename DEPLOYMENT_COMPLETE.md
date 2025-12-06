# 🚀 Complete Deployment Guide

## ✅ Build Status
**Last Build**: Success ✓
**Build Time**: ~2.5 minutes
**Node Version**: 20.17.0
**Docusaurus Version**: 3.9.2

## 📋 Pre-Deployment Checklist

### Frontend (Netlify)
- [x] Build completes successfully
- [x] All dependencies installed
- [x] Netlify configuration file ready
- [x] Environment variables documented
- [ ] Backend API URL configured

### Backend (Python FastAPI)
- [ ] Backend deployed to hosting service
- [ ] Environment variables set
- [ ] Vector database populated
- [ ] CORS configured for frontend domain

## 🌐 Frontend Deployment (Netlify)

### Option 1: Netlify CLI (Recommended)

```powershell
# 1. Install Netlify CLI globally
npm install -g netlify-cli

# 2. Login to Netlify
netlify login

# 3. Build the project
npm run build

# 4. Deploy to production
netlify deploy --prod --dir=build
```

### Option 2: GitHub Integration (Automated)

1. **Push to GitHub**:
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

2. **Connect to Netlify**:
   - Go to https://app.netlify.com
   - Click "Add new site" → "Import an existing project"
   - Choose GitHub and select your repository
   - Build settings are auto-detected from `netlify.toml`

3. **Configure Environment Variables**:
   - Go to Site settings → Build & deploy → Environment
   - Add: `REACT_APP_API_URL` = `https://your-backend-url.com`
   - Trigger a new deploy

### Option 3: Manual Drag & Drop

1. Build locally: `npm run build`
2. Go to https://app.netlify.com
3. Drag and drop the `build` folder

## 🐍 Backend Deployment

### Option 1: Render.com (Free Tier Available)

1. **Create Account**: Go to https://render.com

2. **Create New Web Service**:
   - Connect your GitHub repository
   - Set **Root Directory**: `backend`
   - Set **Environment**: Python 3
   - Set **Build Command**: `pip install -r requirements.txt`
   - Set **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Environment Variables**:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   QDRANT_URL=:memory:
   ```

4. **Deploy**: Click "Create Web Service"

5. **Get URL**: Copy your service URL (e.g., `https://your-app.onrender.com`)

### Option 2: Railway.app

1. **Create Account**: Go to https://railway.app

2. **New Project**:
   - Connect GitHub repository
   - Select the `backend` directory
   - Railway auto-detects Python

3. **Environment Variables**:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Deploy**: Automatic on push

### Option 3: Google Cloud Run

```bash
# 1. Build container
cd backend
gcloud builds submit --tag gcr.io/PROJECT_ID/rag-backend

# 2. Deploy
gcloud run deploy rag-backend \
  --image gcr.io/PROJECT_ID/rag-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_key
```

## 🔧 Post-Deployment Configuration

### 1. Update Frontend with Backend URL

After deploying the backend, update Netlify environment variables:

1. Go to Netlify Dashboard → Site settings → Environment variables
2. Add/Update: `REACT_APP_API_URL` = `https://your-backend-url.com`
3. Trigger redeploy: Deploys → Trigger deploy → Deploy site

### 2. Populate Vector Database

If using persistent storage, run the ingestion script:

```bash
# SSH into your backend server or run locally pointing to production DB
python backend/ingest.py
```

### 3. Test the Chatbot

1. Visit your deployed site
2. Click the "Ask AI" button
3. Check connection status (should show 🟢)
4. Ask a test question
5. Verify response quality

## 🔍 Troubleshooting

### Build Fails on Netlify

**Issue**: Module not found errors
**Solution**: 
```bash
# Clear cache and rebuild
npm run clear
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
npm run build
```

**Issue**: Deprecation warnings
**Solution**: These are warnings, not errors. Build will still succeed.

### Chatbot Shows Disconnected (🔴)

**Issue**: Backend not accessible
**Solutions**:
1. Check backend is deployed and running
2. Verify CORS settings allow your Netlify domain
3. Check `REACT_APP_API_URL` environment variable
4. Test backend health endpoint: `https://your-backend-url.com/health`

### Backend Errors

**Issue**: "GEMINI_API_KEY not set"
**Solution**: Add environment variable in hosting platform

**Issue**: "Collection not found"
**Solution**: Run `python backend/ingest.py` to populate database

**Issue**: Rate limit errors
**Solution**: Implement caching or upgrade Gemini API tier

### Chat Responses Are Poor Quality

**Solutions**:
1. Ensure vector database is populated with course content
2. Check that documents are being retrieved (check backend logs)
3. Adjust retrieval limit in `main.py` (currently 5)
4. Improve chunking strategy in `ingest.py`

## 📊 Monitoring

### Frontend (Netlify)
- **Deploy Logs**: Netlify Dashboard → Deploys → [Latest Deploy] → Deploy log
- **Function Logs**: Not applicable (static site)
- **Analytics**: Netlify Analytics (paid feature)

### Backend
- **Render.com**: Dashboard → Logs tab
- **Railway.app**: Dashboard → Deployments → Logs
- **Google Cloud**: Cloud Console → Cloud Run → Logs

### Performance
- **Lighthouse**: Run `npm run lighthouse` locally
- **Page Speed**: https://pagespeed.web.dev/
- **Uptime**: Use UptimeRobot or similar service

## 🔐 Security Checklist

- [x] HTTPS enabled (automatic on Netlify)
- [x] Security headers configured
- [x] API keys stored in environment variables (not in code)
- [x] CORS properly configured
- [ ] Rate limiting on backend (recommended)
- [ ] Input validation (implemented)
- [ ] Content Security Policy (optional)

## 📈 Optimization Tips

### Frontend
1. **Enable Netlify CDN**: Automatic
2. **Compress Images**: Use WebP format
3. **Code Splitting**: Automatic with Docusaurus
4. **Lazy Loading**: Implemented for chat widget

### Backend
1. **Caching**: Implement Redis for frequent queries
2. **Connection Pooling**: For database connections
3. **Async Processing**: Already using FastAPI async
4. **Rate Limiting**: Add middleware

## 🎯 Success Criteria

Your deployment is successful when:
- ✅ Frontend loads without errors
- ✅ All pages are accessible
- ✅ Chatbot shows connected status (🟢)
- ✅ Chatbot responds to questions
- ✅ Responses are relevant and well-formatted
- ✅ Page load time < 3 seconds
- ✅ Mobile responsive
- ✅ No console errors

## 📞 Support

If you encounter issues:
1. Check deployment logs
2. Review browser console for errors
3. Test backend health endpoint
4. Verify environment variables
5. Check CORS configuration

## 🔄 Continuous Deployment

Once set up with GitHub integration:
1. Make changes locally
2. Commit and push to main branch
3. Netlify automatically rebuilds and deploys
4. Backend redeploys on push (if using Render/Railway)

## 📝 Environment Variables Reference

### Frontend (Netlify)
```
REACT_APP_API_URL=https://your-backend-url.com
```

### Backend (Render/Railway/Cloud Run)
```
GEMINI_API_KEY=your_gemini_api_key_here
QDRANT_URL=:memory:  # or your Qdrant cloud URL
QDRANT_API_KEY=your_qdrant_key  # if using Qdrant cloud
```

## 🎉 Next Steps

After successful deployment:
1. Set up custom domain (optional)
2. Configure analytics
3. Set up monitoring/alerts
4. Plan content updates
5. Gather user feedback
6. Iterate and improve

---

**Last Updated**: 2025-12-06
**Status**: Ready for Production ✅
