# 🚑 Fixing 404 Errors on GitHub Pages

If you are seeing a 404 error, please check these 3 things in order:

## 1. Verify Repository Settings (Most Common!)
**You MUST do this manually.**
1. Open [Repository Settings -> Pages](https://github.com/syedabdullaharmy/Physical-AI-Humanoid-Robotics-Course/settings/pages)
2. Look at **"Build and deployment"**
3. Ensure **Source** is `Deploy from a branch`
4. Ensure **Branch** is `gh-pages` and folder is `/ (root)`
5. **Click SAVE** if you changed anything.

## 2. Verify Your URL (Case Sensitive!)
Your repository name has **Capital Letters**. Your URL must match exactly.

❌ **Wrong**: `.../physical-ai-humanoid-robotics-course/`
✅ **Right**: `.../Physical-AI-Humanoid-Robotics-Course/`

**Correct Link**:
[https://syedabdullaharmy.github.io/Physical-AI-Humanoid-Robotics-Course/](https://syedabdullaharmy.github.io/Physical-AI-Humanoid-Robotics-Course/)

## 3. Wait for Deployment
When I push code (like I just did), it takes **2-3 minutes** for:
1. GitHub Actions to build the site (Orange/Green dot on repo)
2. GitHub Pages to deploy the built files

## What I Just Fixed
I pushed a configuration change (`trailingSlash: false`) which force-fixes many Docusaurus 404 issues on GitHub Pages. 

**Wait 3 minutes from now (until 2:20 PM) and try the link again.**
