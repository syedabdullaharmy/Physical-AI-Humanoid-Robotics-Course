# Deployment Guide for Netlify

## Prerequisites
- Node.js 18 or higher
- npm or yarn
- Netlify account

## Local Development

### 1. Install Dependencies
```bash
npm install
```

### 2. Set up Backend (RAG Chatbot)

#### Install Python Dependencies
```bash
pip install -r backend/requirements.txt
```

#### Configure Environment Variables
Create a `.env` file in the root directory with:
```
GEMINI_API_KEY=your_gemini_api_key
QDRANT_URL=your_qdrant_url (optional, uses local storage if not set)
QDRANT_API_KEY=your_qdrant_api_key (optional)
```

#### Ingest Documentation into Vector Database
```bash
python backend/ingest.py
```

#### Start Backend Server
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Start Frontend Development Server
```bash
npm start
```

## Deployment to Netlify

### Option 1: Deploy via Netlify CLI

1. **Install Netlify CLI**
```bash
npm install -g netlify-cli
```

2. **Login to Netlify**
```bash
netlify login
```

3. **Build the Project**
```bash
npm run build
```

4. **Deploy**
```bash
netlify deploy --prod
```

### Option 2: Deploy via Netlify Dashboard

1. **Build the Project Locally**
```bash
npm run build
```

2. **Go to Netlify Dashboard**
   - Visit https://app.netlify.com
   - Click "Add new site" → "Deploy manually"
   - Drag and drop the `build` folder

### Option 3: Connect GitHub Repository (Recommended)

1. **Push to GitHub**
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

2. **Connect to Netlify**
   - Go to https://app.netlify.com
   - Click "Add new site" → "Import an existing project"
   - Choose GitHub and select your repository
   - Build settings are already configured in `netlify.toml`

## Important Notes

### Backend Deployment
⚠️ **Note**: The Python backend (RAG chatbot) needs to be deployed separately as Netlify only hosts static sites.

**Options for Backend:**
1. **Render.com** (Recommended for free tier)
   - Create a new Web Service
   - Connect your GitHub repo
   - Set root directory to `backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

2. **Railway.app**
   - Similar setup to Render
   - Automatic deployments from GitHub

3. **Google Cloud Run** or **AWS Lambda**
   - For production deployments

### Update Frontend API URL
After deploying the backend, update the API URL in:
`src/components/ChatWidget/index.js`

Change:
```javascript
const response = await fetch('http://127.0.0.1:8000/chat', {
```

To:
```javascript
const response = await fetch('https://your-backend-url.com/chat', {
```

## Environment Variables on Netlify

If you need environment variables for the frontend:
1. Go to Site settings → Build & deploy → Environment
2. Add your variables

## Troubleshooting

### Build Fails
- Check Node.js version (should be 18+)
- Clear cache: `npm run clear`
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`

### 404 Errors
- The `_redirects` file in `static/` handles SPA routing
- Ensure it's copied to the build folder

### Chatbot Not Working
- Verify backend is deployed and running
- Check API URL in ChatWidget component
- Verify CORS settings in backend allow your Netlify domain

## Performance Optimization

The site includes:
- ✅ Lighthouse CI configuration
- ✅ Optimized caching headers
- ✅ Security headers
- ✅ SEO metadata

## Support

For issues, check:
- Netlify deploy logs
- Browser console for frontend errors
- Backend logs for API errors
