# Vercel Deployment - Quick Setup Guide

## 🚀 Deploy to Vercel in 5 Minutes

### Step 1: Import Your Repository

1. Go to [Vercel](https://vercel.com)
2. Click **Add New** → **Project**
3. **Import Git Repository**:
   - Select **GitHub**
   - Find: `syedabdullaharmy/Physical-AI-Humanoid-Robotics-Course`
   - Click **Import**

### Step 2: Configure Project

Vercel will auto-detect Docusaurus. Verify these settings:

**Framework Preset**: Docusaurus ✅ (auto-detected)

**Root Directory**: `./` (leave as default)

**Build Command**: 
```bash
cd frontend && npm run build
```
✅ Already configured in `vercel.json`

**Output Directory**: 
```
frontend/build
```
✅ Already configured in `vercel.json`

**Install Command**:
```bash
cd frontend && npm install
```
✅ Already configured in `vercel.json`

### Step 3: Add Environment Variables

Click **Environment Variables** and add:

| Name | Value | Environment |
|------|-------|-------------|
| `REACT_APP_API_URL` | Your backend API URL | Production, Preview, Development |

Example value: `https://your-backend.railway.app`

### Step 4: Deploy!

1. Click **Deploy**
2. Vercel will build and deploy your site
3. Wait 2-3 minutes for deployment to complete

### Step 5: Access Your Site

Your site will be live at:
```
https://physical-ai-humanoid-robotics-course.vercel.app
```

Or a custom URL assigned by Vercel.

## ✨ Additional Configuration

### Custom Domain (Optional)

1. Go to Project Settings → **Domains**
2. Click **Add Domain**
3. Enter your domain name
4. Follow DNS configuration instructions

### Environment Variables Management

To update environment variables:
1. Go to Project Settings → **Environment Variables**
2. Edit `REACT_APP_API_URL`
3. Redeploy for changes to take effect

### Automatic Deployments

✅ **Already Configured!**
- Push to `main` → Production deployment
- Pull requests → Preview deployments
- No manual action needed

## 🔧 Backend CORS Configuration

Make sure your backend allows requests from Vercel:

```python
# Example FastAPI CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://syedabdullaharmy.github.io",  # GitHub Pages
        "https://*.vercel.app",  # All Vercel deployments
        "https://your-custom-domain.com",  # Your custom domain
        "http://localhost:3000",  # Local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📊 Monitoring

View deployment logs and analytics:
1. Go to your Vercel dashboard
2. Select your project
3. Click **Deployments** to see all builds
4. Click any deployment to view logs

## 🎉 Success!

Your site is now deployed on both:
- ✅ GitHub Pages: `https://syedabdullaharmy.github.io/Physical-AI-Humanoid-Robotics-Course/`
- ✅ Vercel: `https://your-project.vercel.app`

Both will auto-update when you push to GitHub! 🚀

## Troubleshooting

### Build Fails on Vercel

**Check**:
1. Environment variable `REACT_APP_API_URL` is set
2. Build logs for specific errors
3. Verify `vercel.json` configuration

**Common Issues**:
- Missing environment variables
- Node version mismatch (should be 20+)
- Build command errors

### Site Loads But Chatbot Doesn't Work

**Check**:
1. Backend API is running
2. Backend CORS allows Vercel domain
3. `REACT_APP_API_URL` points to correct backend
4. Network tab in browser DevTools for errors

### Preview Deployments Not Working

**Solution**:
- Ensure environment variables are set for "Preview" environment
- Check branch protection rules don't block previews

---

**Need Help?**
- Check Vercel docs: https://vercel.com/docs
- Review build logs in Vercel dashboard
- Test locally first: `cd frontend && npm run build && npm run serve`
