# Deploy to Netlify - PowerShell Script
# This script automates the deployment process

Write-Host "🚀 Starting Netlify Deployment Process..." -ForegroundColor Cyan

# Step 1: Check if build folder exists
if (Test-Path "build") {
    Write-Host "✅ Build folder found!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Build folder not found. Running build..." -ForegroundColor Yellow
    npm run build
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Build failed!" -ForegroundColor Red
        exit 1
    }
}

# Step 2: Check if Netlify CLI is installed
$netlifyInstalled = Get-Command netlify -ErrorAction SilentlyContinue
if (-not $netlifyInstalled) {
    Write-Host "⚠️  Netlify CLI not found. Installing..." -ForegroundColor Yellow
    npm install -g netlify-cli
}

# Step 3: Login to Netlify
Write-Host "`n📝 Please login to Netlify..." -ForegroundColor Cyan
netlify login

# Step 4: Deploy
Write-Host "`n🚀 Deploying to Netlify..." -ForegroundColor Cyan
netlify deploy --prod --dir=build

Write-Host "`n✅ Deployment complete!" -ForegroundColor Green
Write-Host "`n⚠️  IMPORTANT: Don't forget to:" -ForegroundColor Yellow
Write-Host "1. Deploy your backend to Render.com or similar service" -ForegroundColor White
Write-Host "2. Add REACT_APP_API_URL environment variable in Netlify with your backend URL" -ForegroundColor White
Write-Host "3. Redeploy after adding the environment variable" -ForegroundColor White
