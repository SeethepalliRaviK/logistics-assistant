# Push to GitHub - Logistics Assistant
# Run this PowerShell script to push code to GitHub

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "PUSHING TO GITHUB - LOGISTICS ASSISTANT" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to the directory containing this script (portable - no hardcoded paths)
Set-Location $PSScriptRoot

# Configure git remote
Write-Host "Setting up GitHub remote..." -ForegroundColor Yellow
git remote remove origin 2>$null
git remote add origin https://github.com/SeethepalliRaviK/logistics-assistant.git

# Set main branch
Write-Host "Setting main as default branch..." -ForegroundColor Yellow
git branch -M main

# Push to GitHub
Write-Host ""
Write-Host "Pushing code to GitHub..." -ForegroundColor Yellow
Write-Host "You may be prompted to authenticate with your GitHub credentials." -ForegroundColor Gray
Write-Host ""

git push -u origin main

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ SUCCESSFULLY PUSHED TO GITHUB!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your repository is now at:" -ForegroundColor Green
    Write-Host "https://github.com/SeethepalliRaviK/logistics-assistant" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "NEXT STEP: Deploy to Streamlit Cloud" -ForegroundColor Yellow
    Write-Host "1. Go to https://share.streamlit.io" -ForegroundColor Gray
    Write-Host "2. Click 'New app'" -ForegroundColor Gray
    Write-Host "3. Select your repository" -ForegroundColor Gray
    Write-Host "4. Branch: main, File: app.py" -ForegroundColor Gray
    Write-Host "5. Click Deploy" -ForegroundColor Gray
} else {
    Write-Host "❌ PUSH FAILED" -ForegroundColor Red
    Write-Host "Try running: git push -u origin main" -ForegroundColor Yellow
    Write-Host "And authenticate with your GitHub credentials" -ForegroundColor Gray
}

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
