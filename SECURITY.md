# 🔐 Security & API Key Management Guide

## Your Credentials (Already Configured)

Based on your git configuration:
- **GitHub Username**: `SeethepalliRaviK`

**⚠️ Never share your credentials or your API keys publicly!**

> **Note:** a personal email address should never be written into a tracked file. Git records it
> in the author field of every commit as well, so configure a GitHub `noreply` address if you
> want it kept private.

---

## API Key Security Best Practices

### 1. Never Commit API Keys to Git

Your `.gitignore` file automatically excludes:
```
.streamlit/secrets.toml    # Local secrets file
.env                       # Environment files
.env.local
```

**✅ Do This:**
```bash
# Local testing - secrets are NOT committed
echo 'groq_api_key = "gsk_YOUR_KEY_HERE"' > .streamlit/secrets.toml
```

**❌ Don't Do This:**
```bash
# WRONG - Never hardcode keys in app.py
groq_api_key = "gsk_YOUR_KEY_HERE"  # EXPOSED!
```

---

## Safe Workflows for Different Environments

### Local Development

1. **Get your Groq API key:**
   - Go to https://console.groq.com
   - Sign in or create account (free)
   - Navigate to API Keys
   - Copy your key

2. **Store locally (safely):**
   ```bash
   mkdir -p .streamlit
   echo 'groq_api_key = "gsk_YOUR_KEY_HERE"' > .streamlit/secrets.toml
   ```

3. **Run locally:**
   ```bash
   streamlit run app.py
   ```

4. **Verify `.streamlit/secrets.toml` is in `.gitignore`:**
   ```bash
   cat .gitignore | grep secrets.toml
   # Should show: .streamlit/secrets.toml
   ```

---

### Streamlit Cloud Deployment (Recommended)

**Never paste API keys in code or config files!**

#### Step 1: Create GitHub Repository
```bash
# Initialize remote (add your GitHub repo URL)
git remote add origin https://github.com/SeethepalliRaviK/logistics-assistant.git
git branch -M main
git push -u origin main
```

#### Step 2: Connect to Streamlit Cloud
1. Go to https://share.streamlit.io
2. Click "New app"
3. Select your repository
4. Select branch: `main`
5. Select file: `app.py`
6. Click "Deploy"

#### Step 3: Add API Key Securely (via Dashboard)
1. Once deployed, click the **≡ Menu** (top right)
2. Select **⚙️ Settings**
3. Click **🔑 Secrets**
4. Add your secret:
   ```toml
   groq_api_key = "gsk_YOUR_KEY_HERE"
   ```
5. Click **Save**
6. App restarts and uses the secret

**Why this is safe:**
- API key stored on Streamlit's secure servers (not in code)
- Not visible in GitHub repository
- Encrypted in Streamlit Cloud
- Only accessible to your app

---

### GitHub Actions (CI/CD Pipeline)

For automated testing and deployment:

#### Step 1: Add API Key as Repository Secret
1. Go to your GitHub repository
2. Click **Settings** (top menu)
3. Click **Secrets and variables** → **Actions** (left sidebar)
4. Click **New repository secret**
5. Name: `GROQ_API_KEY`
6. Value: `gsk_YOUR_KEY_HERE`
7. Click **Add secret**

#### Step 2: Access in Workflow
The workflow can safely access it:
```yaml
env:
  GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
```

**Why this is safe:**
- Secrets never logged or printed
- Only accessible during workflow runs
- Masked in logs (shows as `***`)
- Cannot be accessed by forks (unless you enable)

---

## API Key Security Checklist

Before sharing code or deploying:

- [ ] `.streamlit/secrets.toml` is in `.gitignore`
- [ ] No API keys in `app.py`, `core/`, or config files
- [ ] Secrets loaded via `st.secrets` or environment variables
- [ ] `.env` file is in `.gitignore`
- [ ] GitHub has secret configured (for Cloud deployment)
- [ ] No API keys in commit history:
  ```bash
  git log --all --oneline | head -20
  ```
- [ ] Run `git show <commit>` to verify no secrets in commits

---

## Environment Variable Fallback

The app checks for API keys in this order:

```python
# 1. First: Streamlit secrets (.streamlit/secrets.toml)
api_key = st.secrets.get("groq_api_key")

# 2. Second: Environment variable
if not api_key:
    api_key = os.environ.get("GROQ_API_KEY")

# 3. If neither: Error
if not api_key:
    st.error("API Key not found!")
```

---

## Revoking Compromised Keys

If you accidentally expose your API key:

1. **Immediately revoke it:**
   - Go to https://console.groq.com/settings/apikeys
   - Delete the exposed key
   - Create a new key

2. **Update all deployments:**
   - Streamlit Cloud: Update secrets
   - GitHub Actions: Update secret
   - Local: Update `.streamlit/secrets.toml`

3. **Check git history:**
   ```bash
   # Search for exposed key
   git log -p | grep -i "gsk_"
   
   # If found, use git filter-branch or BFG Repo-Cleaner
   # (Advanced: only if key was committed)
   ```

---

## Public Repository Safety

If making your repository public:

✅ **Safe to share:**
- Source code
- Configuration structure
- Architecture diagrams
- Setup instructions
- Database schema

❌ **Never share:**
- `.streamlit/secrets.toml`
- `.env` files
- API keys
- Private credentials
- Database backups (if sensitive)

---

## Incident Response

If you suspect a compromised API key:

1. **Immediately revoke** the key at console.groq.com
2. **Generate new key** 
3. **Update all deployments** within 5 minutes
4. **Monitor usage** for suspicious activity
5. **Check GitHub history** for exposed keys
6. **Rotate secrets** in all environments

---

## Additional Security Tips

1. **Use Streamlit Cloud Secrets**
   - More secure than GitHub Actions secrets
   - No exposure in workflow logs
   - Managed by Streamlit's infrastructure

2. **Rotate Keys Periodically**
   - Generate new key every 90 days
   - Delete old keys
   - Update deployments

3. **Monitor API Usage**
   - Go to https://console.groq.com/usage
   - Check for unusual activity
   - Set up alerts if available

4. **Limit Scope**
   - Use API keys only where needed
   - Don't use same key everywhere
   - Consider separate keys for dev/prod

5. **Audit Access**
   - Review GitHub collaborators
   - Check Streamlit Cloud team access
   - Remove old/unused accounts

---

## Troubleshooting

### "GROQ_API_KEY not set"
```bash
# Check local secrets
cat .streamlit/secrets.toml

# Check environment variable
echo $GROQ_API_KEY

# For Streamlit Cloud: Verify in Settings → Secrets
```

### Key rotated but app still fails
- Streamlit Cloud: Wait 2 minutes for app to restart
- Local: Restart the app
- GitHub Actions: Re-run workflow

### Accidentally committed API key
```bash
# Option 1: Delete and recommit (if not pushed)
git reset HEAD~1

# Option 2: Remove from history (if pushed)
# Use: git filter-branch or BFG Repo-Cleaner
# Then push with: git push origin --force-with-lease

# Option 3: Immediately revoke the key
# (at console.groq.com)
```

---

## Resources

- [Groq Security Docs](https://console.groq.com/docs/security)
- [Streamlit Secrets](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management)
- [GitHub Actions Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [OWASP API Security](https://owasp.org/www-project-api-security/)

---

**Last Updated:** September 26, 2026
