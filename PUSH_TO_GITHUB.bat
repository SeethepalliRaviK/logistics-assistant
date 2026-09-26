@echo off
REM Push to GitHub - Run this script to complete deployment

echo.
echo ============================================================
echo PUSHING TO GITHUB - LOGISTICS ASSISTANT
echo ============================================================
echo.

REM Navigate to project directory
cd /d "E:\Ravi\learning\REDACTED\bridge course\Advanced Generative AI for Natural Language Processing\Week 2\week 2-guided activity\MLS-2"

REM Add remote (only if not already added)
git remote remove origin 2>nul
git remote add origin https://github.com/SeethepalliRaviK/logistics-assistant.git

REM Change branch to main
git branch -M main

REM Push to GitHub
echo.
echo Pushing code to GitHub...
echo You may be prompted to authenticate with your GitHub credentials.
echo.
git push -u origin main

echo.
echo ============================================================
if %ERRORLEVEL% EQU 0 (
    echo ✅ SUCCESSFULLY PUSHED TO GITHUB!
    echo.
    echo Your repository is now at:
    echo https://github.com/SeethepalliRaviK/logistics-assistant
    echo.
    echo Next step: Deploy to Streamlit Cloud
    echo 1. Go to https://share.streamlit.io
    echo 2. Click "New app"
    echo 3. Select your repository
    echo 4. Branch: main, File: app.py
    echo 5. Click Deploy
) else (
    echo ❌ PUSH FAILED
    echo Try running: git push -u origin main
    echo And authenticate with your GitHub credentials
)
echo ============================================================
echo.

pause
