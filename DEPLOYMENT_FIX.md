# ⚠️ GitHub Pages Deployment Fix

## Issue
GitHub Actions workflow is running but may fail if GitHub Pages isn't properly configured.

## Required Steps to Fix

### Step 1: Enable GitHub Pages (CRITICAL)
1. Go to: https://github.com/syedabdullaharmy/Physical-AI-Humanoid-Robotics-Course/settings/pages
2. Under "Build and deployment":
   - **Source**: Deploy from a branch  
   - **Branch**: gh-pages
   - **Folder**: / (root)
3. Click **Save**

### Step 2: Add Backend API Secret (IMPORTANT)
1. Go to: https://github.com/syedabdullaharmy/Physical-AI-Humanoid-Robotics-Course/settings/secrets/actions
2. Click "New repository secret"
3. Add:
   - **Name**: `BACKEND_API_URL`
   - **Value**: Your backend URL (e.g., `https://your-backend.railway.app`)

### Step 3: Verify Workflow
1. Go to: https://github.com/syedabdullaharmy/Physical-AI-Humanoid-Robotics-Course/actions
2. Find the latest "Deploy to GitHub Pages" workflow
3. Check if it's:
   - ✅ Running
   - ✅ Success
   - ❌ Failed (if so, click to see logs)

## Common Errors & Fixes

### Error: "gh-pages branch not found"
**Fix**: The workflow will create it automatically on first run. Just wait.

### Error: "Pages build failed"
**Fix**: Ensure Pages is enabled in Settings → Pages

### Error: "BACKEND_API_URL not found"
**Fix**: Add the secret in Settings → Secrets

### Error: Broken links causing build fail
**Status**: Build shows warnings but completes successfully  
**Note**: These are from Docusaurus template files and don't affect deployment

## Current Build Status

✅ **Local Build**: SUCCESS  
✅ **Code Pushed**: Commit `e5f934c`  
⏳ **GitHub Actions**: Check status at actions page  
⏳ **GitHub Pages**: Needs configuration (see Step 1)

## Once Configured

After you complete Steps 1 & 2, the site will be live at:
```
https://syedabdullaharmy.github.io/Physical-AI-Humanoid-Robotics-Course/
```

## Alternative: Manual Trigger

If automatic deployment isn't working:
1. Go to Actions tab
2. Select "Deploy to GitHub Pages" workflow
3. Click "Run workflow" button
4. Select "main" branch
5. Click "Run workflow"

---

**Quick Links**:
- Pages Settings: https://github.com/syedabdullaharmy/Physical-AI-Humanoid-Robotics-Course/settings/pages
- Secrets: https://github.com/syedabdullaharmy/Physical-AI-Humanoid-Robotics-Course/settings/secrets/actions  
- Actions: https://github.com/syedabdullaharmy/Physical-AI-Humanoid-Robotics-Course/actions

**Need to configure these in your GitHub account** (I can't access them for you)
