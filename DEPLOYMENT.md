# Deployment Guide

## Prerequisites

- GitHub account
- Netlify account
- Railway account (or Render/Vercel)
- Google Gemini API key
- Qdrant Cloud account (free tier)
- Neon Postgres account (free tier)

## Step 1: Set Up Databases

### Qdrant Cloud

1. Go to [cloud.qdrant.io](https://cloud.qdrant.io)
2. Create a free cluster
3. Note your:
   - Cluster URL
   - API Key

### Neon Postgres

1. Go to [neon.tech](https://neon.tech)
2. Create a free project
3. Note your connection string

## Step 2: Get API Keys

### Google Gemini API

1. Go to [ai.google.dev](https://ai.google.dev)
2. Get an API key
3. Note your API key

## Step 3: Deploy Backend

### Option A: Railway

1. Go to [railway.app](https://railway.app)
2. Create new project
3. Connect GitHub repository
4. Select `backend/` as root directory
5. Add environment variables:
   ```
   GEMINI_API_KEY=your_key
   QDRANT_URL=your_url
   QDRANT_API_KEY=your_key
   DATABASE_URL=your_postgres_url
   CORS_ORIGINS=https://your-netlify-domain.netlify.app
   ```
6. Deploy!
7. Note your Railway URL (e.g., `https://your-app.railway.app`)

### Option B: Render

### Option B: Render (Free & Easy)

1. Push your code (including `render.yaml`) to GitHub.
2. Go to [dashboard.render.com/blueprints](https://dashboard.render.com/blueprints)
3. Click **New Blueprint Instance**.
4. Connect your GitHub repository.
5. It will automatically detect `render.yaml`.
6. Click **Apply**.
7. Enter your environment variables in the dashboard when prompted (Gemini Key, Qdrant URL, etc.).
8. Wait for deployment to finish.
9. Copy your new backend URL (e.g., `https://physical-ai-textbook-backend.onrender.com`).

## Step 4: Ingest Content

After backend is deployed, ingest the textbook content:

```bash
# Clone repository locally
git clone your-repo-url
cd your-repo/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GEMINI_API_KEY=your_key
export QDRANT_URL=your_url
export QDRANT_API_KEY=your_key
export DATABASE_URL=your_postgres_url

# Run ingestion
python scripts/ingest_content.py
```

## Step 5: Deploy Frontend

### Netlify

1. Go to [netlify.com](https://netlify.com)
2. Connect GitHub repository
3. Configure build settings:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `frontend/build`
4. Add environment variable:
   ```
   REACT_APP_API_URL=https://your-backend-url.railway.app
   ```
5. Update `netlify.toml` with your backend URL
6. Deploy!

## Step 6: Verify Deployment

1. Visit your Netlify URL
2. Test the chatbot
3. Ask a question
4. Verify you get a response

## Troubleshooting

### CORS Errors

Update backend `CORS_ORIGINS` to include your Netlify domain:

```env
CORS_ORIGINS=https://your-site.netlify.app,http://localhost:3000
```

### Chatbot Not Responding

1. Check backend logs in Railway/Render
2. Verify API URL in frontend environment variables
3. Test backend health endpoint: `https://your-backend-url/health`

### Content Not Found

Run the ingestion script again to populate Qdrant.

## Continuous Deployment

Both Netlify and Railway support automatic deployments:

1. Push to `main` branch
2. Netlify rebuilds frontend
3. Railway rebuilds backend
4. Changes go live automatically!

## Custom Domain (Optional)

### Netlify

1. Go to Domain settings
2. Add custom domain
3. Configure DNS

### Railway

1. Go to Settings → Domains
2. Add custom domain
3. Configure DNS

## Monitoring

- **Netlify**: Built-in analytics and logs
- **Railway**: Metrics and logs dashboard
- **Qdrant**: Cloud dashboard for vector DB stats

## Cost Estimates

- **Qdrant**: Free tier (1GB)
- **Neon**: Free tier (0.5GB)
- **Netlify**: Free tier (100GB bandwidth)
- **Railway**: $5/month after free trial
- **Gemini API**: ~$0.50/month for moderate usage

**Total**: ~$5/month (or $0 with free tiers only)

## Security Checklist

- ✅ API keys in environment variables (not in code)
- ✅ CORS configured correctly
- ✅ HTTPS enabled (automatic on Netlify/Railway)
- ✅ Rate limiting enabled
- ✅ Input validation in place

## Next Steps

1. Monitor usage and costs
2. Gather user feedback
3. Iterate on content
4. Add more features!

---

**Congratulations!** Your Physical AI textbook is now live! 🎉
