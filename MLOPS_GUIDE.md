# 🚀 MLOPS GUIDE - Infrastructure & Deployment

**Version**: 1.0  
**Last Updated**: September 26, 2026  
**For**: DevOps engineers, ML engineers, system administrators

---

## 📖 Table of Contents

1. [Deployment Architecture](#deployment-architecture)
2. [Infrastructure Setup](#infrastructure-setup)
3. [CI/CD Pipeline](#cicd-pipeline)
4. [Monitoring & Alerting](#monitoring--alerting)
5. [Scaling Considerations](#scaling-considerations)
6. [Security Hardening](#security-hardening)
7. [Disaster Recovery](#disaster-recovery)
8. [Known Issues & Fixes](#known-issues--fixes)

---

## 🏗️ Deployment Architecture

### **Current Architecture**

```
┌──────────────────────────────────────────────────────────────┐
│                    GITHUB REPOSITORY                         │
│    https://github.com/SeethepalliRaviK/logistics-assistant   │
└──────────────────────────────────────────────────────────────┘
                           │
                           │ (git push)
                           ▼
┌──────────────────────────────────────────────────────────────┐
│              STREAMLIT CLOUD PLATFORM                        │
│  https://[username]-logistics-assistant.streamlit.app        │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Python 3.11.9 Runtime                   │   │
│  │  ┌─────────────────────────────────────────────────┐ │   │
│  │  │           Streamlit Application                 │ │   │
│  │  │  ┌──────────────┐  ┌──────────────┐            │ │   │
│  │  │  │ Compliance   │  │   Product    │            │ │   │
│  │  │  │  Lookup      │  │    Search    │            │ │   │
│  │  │  └──────────────┘  └──────────────┘            │ │   │
│  │  │        │                │                      │ │   │
│  │  │        └────────┬───────┘                      │ │   │
│  │  │                 ▼                              │ │   │
│  │  │        Core Logic (LLM, DB, Tools)            │ │   │
│  │  └─────────────────────────────────────────────────┘ │   │
│  │                     │                              │   │
│  └─────────────────────┼──────────────────────────────┘   │
│                        │                                   │
│        ┌───────────────┼───────────────┐                  │
│        │               │               │                  │
│        ▼               ▼               ▼                  │
│   ┌─────────┐   ┌─────────────┐  ┌─────────────┐         │
│   │Groq API │   │SQLite DB    │  │Cache/Secrets│         │
│   │External │   │(data/)      │  │(Streamlit)  │         │
│   └─────────┘   └─────────────┘  └─────────────┘         │
└──────────────────────────────────────────────────────────┘
```

### **Component Stack**

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Web Server | Streamlit | >=1.28.0 | Frontend + backend |
| Python Runtime | Python | 3.11.9 | Application runtime |
| LLM API | Groq Cloud | Latest | Language model |
| Database | SQLite | Built-in | Product data |
| Web Search | DuckDuckGo | >=3.9.11 | Compliance info |
| Framework | LangChain | 0.3.27 | LLM orchestration |
| Agent | LangGraph | 0.6.6 | ReAct reasoning |
| Hosting | Streamlit Cloud | Cloud | Managed hosting |
| Source Control | GitHub | Cloud | Version control |

---

## ⚙️ Infrastructure Setup

### **Prerequisites**

**For Local Development:**
- Python 3.11.9+
- Git 2.30+
- pip 22.0+

**For Cloud Deployment:**
- GitHub account
- Streamlit Cloud account (free tier available)
- Groq API account with API key

### **Local Setup**

```bash
# 1. Clone repository
git clone https://github.com/SeethepalliRaviK/logistics-assistant.git
cd logistics-assistant

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create secrets file
mkdir -p .streamlit
cat > .streamlit/secrets.toml << EOF
groq_api_key = "gsk_your_key_here"
EOF

# 5. Run app
streamlit run app.py
```

### **Cloud Setup - Streamlit Cloud**

**Advantages:**
- ✅ Free tier available
- ✅ Automatic scaling
- ✅ Built-in SSL/HTTPS
- ✅ GitHub integration (auto-deploy on push)
- ✅ Secrets management
- ✅ Monitoring dashboard

**Setup Steps:**

1. **Create App on Streamlit Cloud**
```
https://share.streamlit.io → New App → GitHub → Select Repo
```

2. **Configure Secrets**
```
Settings → Secrets → Add groq_api_key
```

3. **Auto-Deploy Configuration**
```yaml
# Automatic on every git push to main branch
# No additional setup needed!
```

**Environment Variables Available:**
```
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
PYTHONUNBUFFERED=1
```

---

## 🔄 CI/CD Pipeline

### **GitHub Actions Workflow**

**File**: `.github/workflows/deploy.yml`

**Triggers**:
- On push to `main` branch
- Manual trigger via GitHub UI

**Pipeline Stages:**

```yaml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  test-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
      # 1. Checkout code
      - uses: actions/checkout@v3
      
      # 2. Setup Python 3.11
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      # 3. Install dependencies
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      # 4. Run tests
      - name: Run tests
        run: python -m pytest tests/ -v --tb=short
      
      # 5. Security scan
      - name: Security scan
        run: |
          pip install bandit
          bandit -r core/ -ll
      
      # 6. Verify structure
      - name: Verify structure
        run: |
          [ -f app.py ] && echo "✓ app.py exists"
          [ -d core ] && echo "✓ core/ exists"
          [ -f data/greatglobe.db ] && echo "✓ database exists"
      
      # 7. Deploy (automatic via Streamlit Cloud webhook)
      - name: Trigger Streamlit Cloud build
        if: success()
        run: echo "✓ Deployment triggered on push"
```

**Pipeline Status Checks:**

| Check | Pass Criteria | Action on Fail |
|-------|---|---|
| Python tests | 80+ tests pass | Block merge |
| Code security | No critical issues | Block merge |
| File structure | All files present | Block merge |
| Dependencies | All installed | Block merge |
| Python version | 3.11+ detected | Block merge |

### **Deployment Flow**

```
1. Developer commits & pushes to main
                    │
                    ▼
2. GitHub Actions workflow triggered
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
    Run Tests  Security Scan  Verify Files
        │           │           │
        └───────────┼───────────┘
                    │
        All checks pass?
        │           │
      No          Yes
        │           │
        ▼           ▼
    Fail Build  Trigger Streamlit Cloud
                deployment
                    │
                    ▼
              App rebuilds & deploys
                    │
                    ▼
              Health check
                    │
                    ▼
              Go live (5-10 min)
```

---

## 📊 Monitoring & Alerting

### **Metrics to Monitor**

**Performance Metrics:**
```
- API Response Time: Target <20s for compliance lookup
- Token Usage: Monitor 60-second rolling window
- Database Query Time: Target <100ms
- Cache Hit Rate: Target >80%
- Web Search Latency: Target <5s
```

**Availability Metrics:**
```
- Uptime: Target 99.5%
- Error Rate: Target <0.1%
- Failed Requests: Alert if >5/hour
- API Connection Status: Check every 5 min
```

**Resource Metrics:**
```
- Memory Usage: Alert if >512MB
- CPU Usage: Alert if >80%
- Disk Usage: Alert if >90%
```

### **Streamlit Cloud Dashboard**

**Access**: `share.streamlit.io` → Your App → Info

**Metrics Available:**
- App runs per month
- Unique users per month
- Deployment status
- Error logs
- Performance timeline

### **Log Monitoring**

**View Logs:**
```bash
# Local development
streamlit run app.py --logger.level=debug

# Streamlit Cloud
Settings → Logs tab
```

**Log Levels:**
```
DEBUG: Detailed information (development)
INFO: General information (normal operation)
WARNING: Something unexpected (not an error)
ERROR: Error occurred (needs attention)
CRITICAL: System failure (needs immediate action)
```

### **Custom Monitoring Script**

```python
# monitor.py
import requests
import time
from datetime import datetime

def health_check(url):
    """Check app health"""
    try:
        response = requests.get(url, timeout=5)
        return {
            'status': 'healthy' if response.status_code == 200 else 'unhealthy',
            'response_time': response.elapsed.total_seconds(),
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

# Monitor every 5 minutes
while True:
    health = health_check('https://logistics-assistant.streamlit.app')
    print(f"[{health['timestamp']}] Status: {health['status']}")
    time.sleep(300)  # 5 minutes
```

---

## 📈 Scaling Considerations

### **Current Capacity**

**Single Instance (Streamlit Cloud Free):**
- ~100 concurrent users
- ~1000 requests/hour
- ~50GB bandwidth/month
- ~500MB memory

**For Higher Load:**

| Load Level | Users | Requests/Hour | Solution |
|-----------|-------|---|---|
| Small | <100 | <1000 | Streamlit Free |
| Medium | 100-1K | 1K-10K | Streamlit Pro |
| Large | 1K-10K | 10K-100K | Docker on cloud |
| Enterprise | 10K+ | 100K+ | Multi-instance |

### **Scaling Strategy**

**Phase 1: Current (Streamlit Cloud Free)**
```
Single app instance
Max 100 concurrent users
No caching infrastructure
```

**Phase 2: Upgrade to Streamlit Pro ($20/month)**
```
Priority deployment queue
Better performance
Remove Streamlit ads
Reach 500+ concurrent users
```

**Phase 3: Custom Deployment (Docker + Cloud)**
```
Docker containerization
Load balancer
Redis caching
Multiple instances (Kubernetes)
Reach 10K+ concurrent users
```

### **Database Scaling**

**Current: SQLite**
- Single file database
- Good for <1000 concurrent
- Suitable for current load

**Future: PostgreSQL**
```bash
# When SQLite becomes bottleneck
pip install psycopg2
# Update database.py to use PostgreSQL connection
```

---

## 🔐 Security Hardening

### **API Key Management**

**Current Implementation:**
```
Development:  .streamlit/secrets.toml (local, in .gitignore)
Production:   Streamlit Cloud Secrets (encrypted)
CI/CD:        GitHub Actions Secrets (encrypted)
```

**Best Practices:**
```
✅ Never commit API keys
✅ Use environment variables
✅ Rotate keys regularly
✅ Use principle of least privilege
✅ Monitor API key usage
❌ Never share keys in Slack/Email
❌ Never hardcode in source code
❌ Never share with unauthorized users
```

### **Database Security**

```python
# Secure database connection
def get_connection():
    # Use SQLite in WAL mode for concurrency
    conn = sqlite3.connect('data/greatglobe.db')
    conn.execute('PRAGMA journal_mode=WAL')
    
    # Enable foreign keys
    conn.execute('PRAGMA foreign_keys=ON')
    
    # Set timeout
    conn.timeout = 5.0
    
    return conn

# Prevent SQL injection
def safe_query(query, params):
    # Always use parameterized queries
    cursor.execute(query, params)  # ✅ Safe
    # NOT: cursor.execute(f"SELECT * WHERE id={id}")  # ❌ Unsafe
```

### **Web Application Security**

```python
# OWASP Top 10 Protections

# 1. Input Validation
validate_product_id(user_input)
validate_country(user_input)

# 2. SQL Injection Prevention
# Using parameterized queries ✅

# 3. XSS Prevention
# Streamlit auto-escapes HTML ✅

# 4. CSRF Protection
# Streamlit handles this ✅

# 5. Rate Limiting
TokenBudget class implements rate limiting ✅

# 6. Authentication
# Groq API key in secure storage ✅

# 7. Secure Headers
# Streamlit Cloud provides HTTPS ✅

# 8. Dependency Scanning
# Regular updates via GitHub Dependabot ✅
```

### **Enable GitHub Security Features**

```bash
# 1. Enable branch protection
Settings → Branches → Add rule for 'main'
  - Require PR review
  - Require status checks
  - Dismiss stale PR approvals

# 2. Enable Dependabot
Settings → Security & analysis → Enable Dependabot

# 3. Enable Secret scanning
Settings → Security & analysis → Enable secret scanning

# 4. Set up CODEOWNERS
# Create .github/CODEOWNERS
* @SeethepalliRaviK
```

---

## 🔄 Disaster Recovery

### **Backup Strategy**

**Automatic Backups:**
```bash
# Database backup (daily)
0 0 * * * tar -czf /backups/db_backup_$(date +%Y%m%d).tar.gz data/

# Code backup (via GitHub)
# Automatic: GitHub keeps 3 months of history
```

**Manual Backup:**
```bash
# Backup database
cp data/greatglobe.db data/greatglobe.db.backup_$(date +%Y%m%d)

# Backup configuration
cp .streamlit/config.toml .streamlit/config.toml.backup

# Backup entire project
tar -czf logistics-assistant_backup_$(date +%Y%m%d).tar.gz .
```

### **Recovery Procedures**

**Scenario 1: App Crashes**
```
1. Check Streamlit Cloud dashboard
2. View error logs
3. If code issue:
   - Fix in repository
   - git commit && git push
   - Streamlit auto-deploys (5-10 min)
4. If not code issue:
   - Restart app from dashboard
   - Monitor for 5 minutes
   - Escalate if persists
```

**Scenario 2: Database Corrupted**
```
1. Stop app (disable from Streamlit dashboard)
2. Restore from backup:
   cp data/greatglobe.db.backup data/greatglobe.db
3. Verify database integrity:
   sqlite3 data/greatglobe.db "PRAGMA integrity_check;"
4. Restart app
5. Test basic functionality
```

**Scenario 3: API Key Compromised**
```
1. Revoke old key:
   console.groq.com → Settings → API Keys → Delete
2. Create new key
3. Update secrets:
   - Local: .streamlit/secrets.toml
   - Production: Streamlit Cloud → Settings → Secrets
   - CI/CD: GitHub → Settings → Secrets
4. Redeploy all systems
5. Monitor API usage for unauthorized access
```

**Scenario 4: GitHub Repository Compromised**
```
1. Remove sensitive files
2. Audit git history:
   git log --all --oneline
3. Force push to remove sensitive commits:
   git filter-branch --tree-filter "rm -f secrets.toml" HEAD
4. Update all secrets
5. Review collaborator access
6. Enable 2FA on GitHub account
```

### **Recovery Time Objectives (RTO)**

| Scenario | Target RTO | Action |
|----------|---|---|
| App crash | <5 min | Auto-restart |
| DB corruption | <15 min | Restore backup |
| API key leak | <30 min | Rotate key |
| Code bug | <30 min | Fix + push |

---

## 🐛 Known Issues & Fixes

### **Issue 1: DDGS Version Incompatibility**

**Symptoms:**
```
ImportError: cannot import name 'DDGS'
or
AttributeError: 'DDGS' object has no attribute 'text'
```

**Root Cause:**
- `ddgs==9.6.1` is outdated
- API changed in newer versions

**Fix:**
```bash
pip install -U duckduckgo-search>=3.9.11
```

**Prevention:**
- Pin to latest version in requirements.txt
- Regular dependency updates

---

### **Issue 2: Python 3.14.7 Incompatibility**

**Symptoms:**
```
ERROR: Could not find a version that satisfies the requirement langchain==0.3.27
or
Module not found: typing_extensions
```

**Root Cause:**
- Many packages not yet compatible with Python 3.14
- Type hints syntax changed

**Fix:**
```bash
# Create runtime.txt
echo "python-3.11.9" > runtime.txt

# Or specify in Streamlit Cloud deployment:
Settings → Advanced → Python version → 3.11
```

**Prevention:**
- Use Python 3.11.9 as standard
- Test upgrades before production

---

### **Issue 3: Streamlit Secrets Not Loaded**

**Symptoms:**
```
Groq API Key not found!
or
KeyError: 'groq_api_key'
```

**Root Cause:**
- Secrets not configured in Streamlit Cloud
- Local `.streamlit/secrets.toml` missing

**Fix:**
```bash
# Local development
mkdir -p .streamlit
echo 'groq_api_key = "gsk_your_key"' > .streamlit/secrets.toml

# Production
Settings → Secrets → Add groq_api_key
```

**Prevention:**
- Verify secrets before deployment
- Use health check page
- Alert on missing secrets

---

### **Issue 4: Database Lock Timeout**

**Symptoms:**
```
sqlite3.OperationalError: database is locked
```

**Root Cause:**
- Concurrent writes to SQLite
- Default timeout too short

**Fix:**
```python
conn.timeout = 5.0  # Increase timeout to 5 seconds
conn.execute('PRAGMA journal_mode=WAL')  # Enable WAL mode
```

---

### **Issue 5: API Rate Limiting (429 Errors)**

**Symptoms:**
```
Error 429: Rate limit exceeded
or
Groq API rate limited
```

**Root Cause:**
- Exceeded 8000 TPM limit
- Multiple concurrent requests

**Fix:**
```python
# Automatic in code:
TokenBudget implements rolling window
RateLimitedChatGroq implements automatic retry

# Manual mitigation:
1. Disable ReAct agent toggle
2. Use simple_compliance_lookup instead
3. Wait 60 seconds before retrying
```

**Prevention:**
- Monitor token usage
- Set alerts at 80% usage
- Implement request queuing

---

### **Issue 6: High Memory Usage**

**Symptoms:**
```
MemoryError or app slowdown
or
Streamlit Cloud: "App exceeds memory limit"
```

**Root Cause:**
- Large in-memory objects
- Cache not clearing
- Memory leaks

**Fix:**
```python
# Clear cache periodically
@st.cache_data(ttl=3600)  # Clear after 1 hour

# Stream large results instead of buffering
for result in results:
    st.write(result)

# Limit product queries
get_all_products(limit=100)  # Don't load all at once
```

---

### **Issue 7: Slow Response Times (>60s)**

**Symptoms:**
```
App timeout or "Streamlit server didn't respond"
```

**Root Cause:**
- Rate limit waiting (60s)
- Slow network
- Overloaded API

**Fix:**
```python
# Disable agent for faster results
use_agent = st.checkbox("Use ReAct Agent", value=False)

# If rate limit:
# - Wait 60 seconds
# - Reduce TPM usage
# - Upgrade Groq plan
```

---

## 📋 Maintenance Checklist

**Weekly:**
- [ ] Check app logs for errors
- [ ] Monitor API key usage
- [ ] Verify database integrity
- [ ] Test core functionality

**Monthly:**
- [ ] Review dependency updates
- [ ] Audit access logs
- [ ] Test disaster recovery procedures
- [ ] Update documentation

**Quarterly:**
- [ ] Security audit
- [ ] Performance review
- [ ] Capacity planning
- [ ] Team training

---

**Last Updated**: September 26, 2026  
**Status**: Production Ready  
**Support**: Contact DevOps team
