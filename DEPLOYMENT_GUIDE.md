# 🚀 Deployment Guide

## Your Credentials

**GitHub:**
- **Username**: `SeethepalliRaviK`
- **Already Configured**: ✅ Yes (in git config)

> **Note:** never write a personal email address into a tracked file. Git also records it in the
> author field of every commit, so use a GitHub `noreply` address if you want it kept private.

---

## Step 1: Add Your Groq API Key (Local Testing)

```bash
# Create the secrets file
mkdir -p .streamlit
echo 'groq_api_key = "YOUR_GROQ_API_KEY_HERE"' > .streamlit/secrets.toml

# Replace YOUR_GROQ_API_KEY_HERE with your actual key from https://console.groq.com
```

**Get your Groq API Key:**
1. Go to https://console.groq.com
2. Sign in (or create a free account)
3. Click "API Keys" in the sidebar
4. Copy your key (starts with `gsk_`)
5. Paste into `.streamlit/secrets.toml`

**Verify it works locally:**
```bash
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501 in your browser.

---

## Step 2: Create GitHub Repository

**Option A: Using GitHub Web Interface (Recommended)**

1. Go to https://github.com/new
2. Enter repository name: `logistics-assistant` (or your choice)
3. Description: `Groq-powered Logistics Compliance Assistant with Streamlit`
4. **Public** or **Private** (your choice)
5. ✗ Do NOT initialize with README (we have one)
6. Click "Create repository"

**Option B: Using GitHub CLI**

```bash
gh repo create logistics-assistant --public --source=. --remote=origin --push
```

---

## Step 3: Push Code to GitHub

```bash
# Add the remote (replace with your repo URL)
git remote add origin https://github.com/SeethepalliRaviK/logistics-assistant.git

# Set main as default branch
git branch -M main

# Push your code
git push -u origin main
```

**Verify on GitHub:**
- Go to https://github.com/SeethepalliRaviK/logistics-assistant
- You should see all files (app.py, core/, utils/, etc.)
- **Make sure**: No `.streamlit/secrets.toml` file is there ✓

---

## Step 4: Deploy to Streamlit Cloud

1. **Go to** https://share.streamlit.io
2. **Sign in** with your GitHub account (if not already)
3. Click **New app**
4. **Connect GitHub account** (if prompted)
5. **Select repository:**
   - Repo: `SeethepalliRaviK/logistics-assistant`
   - Branch: `main`
   - File: `app.py`
6. Click **Deploy** (wait 2-3 minutes)

**The app is now live!** You'll see a URL like:
```
https://ravi-logistics-assistant.streamlit.app
```

---

## Step 5: Add API Key to Streamlit Cloud

1. **In your deployed app**, click the **≡ Menu** (top right)
2. Click **⚙️ Settings**
3. Click **🔑 Secrets** (left sidebar)
4. Add:
   ```toml
   groq_api_key = "gsk_YOUR_KEY_HERE"
   ```
5. Click **Save**
6. App will restart and use the secret

**✅ Done!** Your app is now live with the API key.

---

## Step 6: Verify Deployment

- [ ] App loads at https://ravi-logistics-assistant.streamlit.app
- [ ] No errors in the sidebar
- [ ] Can enter Product ID
- [ ] Can search products
- [ ] Compliance lookup works (with your Groq API key)
- [ ] View the debug page to confirm API key is loaded

---

## Updating Your App

**Make changes locally:**
```bash
# Edit any files (e.g., app.py)
nano app.py

# Test locally
streamlit run app.py

# Commit and push
git add .
git commit -m "Update: added new feature"
git push origin main
```

**Streamlit Cloud auto-deploys** within seconds!

---

## GitHub Actions CI/CD

The workflow automatically runs on every push:

```
Your Push → GitHub Actions Tests → Streamlit Cloud Deploy
   ↓              ↓                      ↓
git push     • Lint code          Auto-restart app
            • Verify imports     New URL available
            • Check database
            • Security scan
```

**View workflow status:**
1. Go to your GitHub repo
2. Click **Actions** tab
3. See build history

---

## Troubleshooting

### "GROQ_API_KEY not set" in Streamlit Cloud

**Solution:**
1. Go to Settings → Secrets
2. Verify you added the key
3. Wait 2 minutes for app to restart
4. Refresh the page

### App won't start locally

```bash
# Check if dependencies are installed
pip list | grep streamlit

# Reinstall all
pip install -r requirements.txt --force-reinstall

# Run again
streamlit run app.py
```

### GitHub push fails

```bash
# Verify credentials
git config --list | grep user

# Check remote
git remote -v

# Try again with verbose output
git push -u origin main -v
```

### Database not found

```bash
# Check if data/greatglobe.db exists
ls -la data/

# Should see: data/greatglobe.db

# If missing, database.py will handle it gracefully
```

---

## Security Reminders

✅ **Do:**
- Store API key in `.streamlit/secrets.toml` (local)
- Add API key via Streamlit Cloud dashboard (not in code)
- Keep `.streamlit/secrets.toml` in `.gitignore`
- Rotate API key every 90 days

❌ **Don't:**
- Never hardcode API keys in app.py
- Never commit `.streamlit/secrets.toml`
- Never share API key publicly
- Never paste key in code or chat

---

## Next Steps After Deployment

1. **Share your app:**
   - URL: https://ravi-logistics-assistant.streamlit.app
   - Can share publicly
   - Works in any browser

2. **Monitor API usage:**
   - Go to https://console.groq.com/usage
   - Check Groq token usage
   - Set alerts if needed

3. **Collect user feedback:**
   - Use Streamlit Cloud community features
   - Add feedback button in app
   - Monitor error logs

4. **Make improvements:**
   - Update code locally
   - Test with `streamlit run app.py`
   - Push to GitHub (auto-deploys)

---

## Quick Reference

| Task | Command |
|------|---------|
| Test locally | `streamlit run app.py` |
| Create commit | `git commit -m "message"` |
| Push to GitHub | `git push origin main` |
| View Streamlit Cloud | https://share.streamlit.io |
| View your app | https://ravi-logistics-assistant.streamlit.app |
| Check API usage | https://console.groq.com/usage |
| Add Groq API key | https://console.groq.com/settings/apikeys |

---

## Support

- **Streamlit Docs**: https://docs.streamlit.io
- **Groq API Docs**: https://console.groq.com/docs
- **LangChain Docs**: https://python.langchain.com
- **GitHub Docs**: https://docs.github.com

---

**Last Updated:** September 26, 2026
