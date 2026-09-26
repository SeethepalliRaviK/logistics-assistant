# 🆘 COMPREHENSIVE TROUBLESHOOTING GUIDE

**Version**: 1.0  
**Last Updated**: September 26, 2026  
**For**: All users - End users, developers, operations teams

---

## 📖 Quick Navigation

- [Symptom-Based Troubleshooting](#symptom-based-troubleshooting)
- [Error Code Reference](#error-code-reference)
- [Performance Issues](#performance-issues)
- [Data & Database Issues](#data--database-issues)
- [API & Network Issues](#api--network-issues)
- [Deployment Issues](#deployment-issues)
- [Debug Checklist](#debug-checklist)
- [Escalation Procedure](#escalation-procedure)

---

## 🔍 Symptom-Based Troubleshooting

### **Symptom 1: App Won't Load**

**What You See:**
```
Nothing loads or blank page
Connection timeout
Page takes >30 seconds
```

**Step 1: Check Internet**
```
1. Open https://google.com in browser
2. If loads: Internet OK, continue
3. If fails: No internet - check connection
```

**Step 2: Check App Status**
```
1. Go to: https://share.streamlit.io
2. Find your app in list
3. Look for deployment status
4. Green checkmark = OK
5. Red X = Currently deploying/failed
```

**Step 3: Try Browser Fixes**
```
1. Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
2. Clear cache: Ctrl+Shift+Delete
3. Try different browser (Chrome, Firefox, Edge)
4. Try incognito/private mode
```

**Step 4: Wait for Deployment**
```
If deployed within last 10 minutes:
- Wait 5 more minutes
- Refresh page
- Should load
```

**Step 5: Still Not Loading?**
```
→ Escalate to technical team (see Error Reporting)
→ Include:
  - Screenshot of loading screen
  - Browser console errors (F12 → Console)
  - Deployment logs from Streamlit Cloud
```

---

### **Symptom 2: "Groq API Key not found"**

**What You See:**
```
❌ Groq API Key not found!
Please add your API key:
* Local: Create `.streamlit/secrets.toml`
* Streamlit Cloud: Add via Settings → Secrets
```

**For End Users:**
```
1. Contact your IT team
2. Say: "The app needs Groq API key configured"
3. Ask them to:
   - Go to https://share.streamlit.io
   - Open the app settings
   - Add groq_api_key secret
```

**For Administrators:**
```
1. Go to: https://share.streamlit.io
2. Click your app
3. Click gear icon (Settings)
4. Click "Secrets"
5. Add: groq_api_key = "gsk_YOUR_KEY_HERE"
6. Click Save
7. App restarts automatically
8. Test with compliance lookup
```

---

### **Symptom 3: Product ID Not Found**

**What You See:**
```
⚠️ Product not found: P1001
Please check the product ID and try again.
```

**Step 1: Verify Product ID**
```
1. Check your source document/system
2. Copy product ID exactly
3. Note: Case sensitive! "P1001" ≠ "p1001"
4. Check for extra spaces: "P 1001" should be "P1001"
```

**Step 2: Search for Product**
```
1. Click "Product Search" tab
2. Choose "By Product ID"
3. Enter partial ID (e.g., "P10")
4. Click Search
5. Find correct ID in results
6. Copy exact ID
7. Go back to Compliance Lookup
8. Try again
```

**Step 3: Try Different Product**
```
1. Go to Product Search
2. Click "View All Products"
3. Pick any product ID
4. Try compliance lookup with that ID
5. If works: Original ID doesn't exist
6. If fails: Database issue (escalate)
```

**Step 4: Still Not Working?**
```
→ Product ID might not be in database
→ Contact your inventory team
→ Ask them to:
   - Add product to database
   - Or provide a valid product ID
```

---

### **Symptom 4: Results Take Too Long (Spinning for >30s)**

**What You See:**
```
⏳ "Running..." spinner spinning for too long
Nothing happens after clicking "Get Compliance Info"
```

**Step 1: Check Internet Speed**
```
Go to: https://fast.com
Check if internet speed is:
- Download: >5 Mbps ✓
- Upload: >2 Mbps ✓
If lower: Your internet is slow
→ Move closer to router
→ Restart router
→ Contact ISP
```

**Step 2: Try Fast Mode**
```
1. Uncheck "Use ReAct Agent" toggle
2. Click "Get Compliance Info" again
3. Should respond in 5-10 seconds
4. If fast mode works: Agent is slow (normal)
5. If still slow: Network or API issue
```

**Step 3: Check Token Usage**
```
1. Click "Debug" tab
2. Look at "Token Usage"
3. If near max (6400): API is rate limited
4. Wait 60 seconds
5. Try again
```

**Step 4: Try Different Product**
```
1. Go back to Compliance Lookup
2. Enter different Product ID
3. Try again
4. If works: Previous product was complex
5. If fails: API issue (continue below)
```

**Step 5: Check Groq API Status**
```
1. Click "Debug" tab
2. Look for "API Status"
3. If "Error": Groq API down
4. Wait 10 minutes
5. Try again
```

**Step 6: Still Slow?**
```
→ Groq API is slow (external issue)
→ Try again later
→ Or contact Groq support if persistent
```

---

### **Symptom 5: Error Message with Code**

**What You See:**
```
❌ Error (429)
❌ Error (401)
❌ Error (500)
Something went wrong - please try again
```

**Next Steps:**
→ Find your error code below: [Error Code Reference](#error-code-reference)

---

## 📋 Error Code Reference

### **Error 401: Unauthorized**

**Meaning**: API key is invalid or expired

**Causes:**
```
1. Wrong API key entered
2. API key was revoked
3. API key expired
4. Copy-paste error (extra spaces)
```

**Fix:**
```
1. Go to: console.groq.com
2. Check if API key is still valid
3. If expired/invalid: Create new key
4. Update in Streamlit Cloud Settings → Secrets
5. Test again
```

**For Admins:**
```
streamlit run app.py --logger.level=debug
→ Check error message
→ Verify groq_api_key in environment
```

---

### **Error 429: Rate Limited**

**Meaning**: Too many API requests in short time

**Causes:**
```
1. Exceeded 8,000 tokens per minute
2. Made more than 30 requests per minute
3. Groq's per-request limits exceeded
```

**Fix:**
```
1. Wait 60 seconds
2. Try again
3. Use "Without ReAct Agent" for faster response
4. Don't click button multiple times
```

**To Prevent:**
```
1. Uncheck "Use ReAct Agent"
2. Use simple compliance lookup
3. Wait between searches (5+ seconds)
4. Monitor token usage in Debug tab
```

**For Admins:**
```
# Check token budget
python -c "from core.groq_client import BUDGET; print(BUDGET.used())"

# Increase token budget (NOT RECOMMENDED - costs more)
# In core/groq_client.py:
BUDGET = TokenBudget(max_tokens=7200)  # Increase from 6400
```

---

### **Error 500: Server Error**

**Meaning**: Groq API or internal server error

**Causes:**
```
1. Groq's servers temporarily down
2. Database connection lost
3. Network issue on our end
```

**Fix:**
```
1. Wait 2-3 minutes
2. Refresh page
3. Try again
4. If persists: Groq API is down
   → Check: https://status.groq.com
```

**For Admins:**
```
# Check Streamlit Cloud logs
share.streamlit.io → App → Logs

# Check database
python -c "from core.database import check_database_exists; print(check_database_exists())"
```

---

### **Error 503: Service Unavailable**

**Meaning**: Service temporarily down for maintenance

**Causes:**
```
1. Groq API maintenance
2. Streamlit Cloud maintenance
3. Your internet connection
```

**Fix:**
```
1. Wait 5-10 minutes
2. Check: https://status.groq.com
3. Check: Streamlit Cloud status page
4. Refresh and retry
```

---

### **Error 502: Bad Gateway**

**Meaning**: Communication error between servers

**Causes:**
```
1. Network connectivity issue
2. Proxy/firewall blocking
3. DNS resolution failure
```

**Fix:**
```
1. Hard refresh: Ctrl+Shift+R
2. Try different network (4G instead of WiFi)
3. Try different browser
4. Check firewall/proxy settings
```

---

### **Error SQLite: Database Locked**

**Meaning**: Database is being accessed by another process

**Causes:**
```
1. Multiple requests at same time
2. Previous request didn't finish
3. Database file corrupted
```

**Fix:**
```
1. Refresh page
2. Wait 5 seconds
3. Try again
4. If persists: Restart app
   → Streamlit Cloud: Settings → Rerun
```

---

## ⚡ Performance Issues

### **Issue 1: App is Very Slow**

| Symptom | Cause | Fix |
|---------|-------|-----|
| Takes >30s | Network slow | Check internet speed |
| Spinner spins forever | API down | Check API status |
| Complian ce lookup freezes | Rate limit | Wait 60s |
| Search is slow | Database slow | Upgrade cloud tier |

**Diagnostic Command:**
```bash
# Check API response time
curl -s -o /dev/null -w "%{time_total}s" https://api.groq.com/health

# Check database query time
time python -c "from core.database import get_all_products; get_all_products(limit=10)"
```

---

### **Issue 2: Inconsistent Performance**

**Symptom**: Sometimes fast, sometimes slow

**Cause**: Variable network/API conditions

**Solution**:
```
1. Not a bug - normal behavior
2. Disable ReAct Agent for consistent speed
3. Try during off-peak hours
4. Upgrade to Streamlit Pro for better resources
```

---

## 💾 Data & Database Issues

### **Issue 1: Product Data Missing**

**Problem**: Product exists but not found in search

**Diagnosis:**
```bash
# Check if product in database
sqlite3 data/greatglobe.db "SELECT * FROM products WHERE product_id='P1001';"
```

**Solution:**
```
1. If found: Search issue - try exact ID match
2. If not found: Product not in database
   → Contact database administrator
   → Ask to add product or check ID
```

---

### **Issue 2: Database Corruption**

**Symptoms:**
```
❌ database disk image malformed
❌ database is corrupted
❌ cannot open database
```

**Fix:**
```
# 1. Check integrity
sqlite3 data/greatglobe.db "PRAGMA integrity_check;"

# 2. If corruption found: Restore backup
cp data/greatglobe.db.backup data/greatglobe.db

# 3. Verify
sqlite3 data/greatglobe.db "SELECT COUNT(*) FROM products;"

# 4. Restart app
```

---

## 🌐 API & Network Issues

### **Issue 1: Cannot Connect to Groq API**

**Symptoms:**
```
❌ Connection refused
❌ Connection timeout
❌ Unable to reach api.groq.com
```

**Diagnosis:**
```bash
# Test connection
ping api.groq.com

# Test with curl
curl https://api.groq.com -v

# Check DNS
nslookup api.groq.com
```

**Solutions:**
```
1. Check internet connection
2. Check firewall/proxy settings
3. Try VPN if geo-blocked
4. Check Groq API status page
5. Contact IT if behind corporate proxy
```

---

### **Issue 2: Certificate/SSL Errors**

**Error**: 
```
❌ SSL: CERTIFICATE_VERIFY_FAILED
❌ certificate verify failed
```

**Causes:**
```
1. Antivirus intercepting HTTPS
2. Corporate proxy decrypting traffic
3. System date/time wrong
4. Expired/invalid certificate
```

**Fixes:**
```
1. Check system date/time: Should be current
2. Disable antivirus HTTPS inspection temporarily
3. Contact IT about proxy
4. Update Python certificates:
   pip install --upgrade certifi
```

---

## 🚀 Deployment Issues

### **Issue 1: Deployment Takes >10 Minutes**

**What's Normal:**
```
First deployment: 5-10 minutes
- Provisioning machine
- Installing dependencies
- Building app

Subsequent deployments: 3-5 minutes
- Just code updates
- Faster rebuild
```

**If Takes >15 minutes:**
```
1. Check dependency installation
2. Look at logs for errors
3. Kill and retry deployment
```

---

### **Issue 2: App Works Locally, Fails in Cloud**

**Causes:**
```
1. Missing environment variable
2. Different Python version
3. Database path different
4. Missing file in repository
```

**Debug Steps:**
```bash
# 1. Check Python version locally
python --version

# 2. Verify files in git
git status
git ls-files

# 3. Test with cloud Python version
docker run python:3.11.9 python -m pip install -r requirements.txt

# 4. Check environment variables
echo %GROQ_API_KEY%  # Windows
echo $GROQ_API_KEY   # Mac/Linux

# 5. Verify secrets
cat .streamlit/secrets.toml
```

---

### **Issue 3: GitHub Authentication Fails**

**Error:**
```
fatal: Authentication failed for 'https://github.com/...'
```

**Fix:**
```
1. Use personal access token instead of password:
   - Settings → Developer settings → Personal access tokens
   - Generate new token (with 'repo' scope)
   - Use token as password

2. Or use SSH:
   - Setup SSH key
   - Use git@github.com:username/repo.git

3. Store credentials:
   - Windows: Use Credential Manager
   - Mac: Use keychain
   - Linux: Use git credential helper
```

---

## 📋 Debug Checklist

**For End Users (Encountering Errors):**

- [ ] **Screenshot error message** (exact text)
- [ ] **Note date & time** of error
- [ ] **Try refreshing** the page
- [ ] **Click "Debug" tab** and screenshot
- [ ] **Write down what you did** before error
- [ ] **Try again** with different product ID
- [ ] **Document findings** to share with team

**For Developers (Debugging Code):**

- [ ] **Check logs**: `streamlit run app.py --logger.level=debug`
- [ ] **Add print statements**: `print(f"Debug: {variable}")`
- [ ] **Use Python debugger**: `import pdb; pdb.set_trace()`
- [ ] **Check imports**: `python -c "import core.groq_client"`
- [ ] **Verify database**: `sqlite3 data/greatglobe.db ".tables"`
- [ ] **Test API key**: `curl -H "Authorization: Bearer $GROQ_API_KEY" https://api.groq.com/health`
- [ ] **Monitor resources**: `top` (CPU/memory usage)
- [ ] **Check network**: `netstat -an | grep 8501`

**For Operations (Deployment Issues):**

- [ ] **Check app logs**: Share.streamlit.io → Logs
- [ ] **Verify secrets**: Settings → Secrets → Verify all keys
- [ ] **Check Python version**: `python --version` should be 3.11.9
- [ ] **Verify files**: All required files in repository
- [ ] **Test dependencies**: `pip install -r requirements.txt`
- [ ] **Check database**: `ls -la data/greatglobe.db`
- [ ] **Monitor system**: Memory, CPU, disk usage
- [ ] **Review git history**: `git log --oneline -10`

---

## 📧 Escalation Procedure

**Step 1: Gather Evidence**

```
✓ Error message (exact text, screenshot)
✓ Date and time of error
✓ Steps to reproduce
✓ Debug page screenshot
✓ Browser and OS information
✓ Attachments: screenshots, logs
```

**Step 2: Document Issue**

```
ISSUE REPORT
=============

Title: [Brief description]
Severity: Critical / High / Medium / Low

DESCRIPTION:
[What happened, what you expected]

REPRODUCTION STEPS:
1. Click "Compliance Lookup"
2. Enter Product ID: [ID]
3. Click "Get Compliance Info"
4. See error: [Error text]

ENVIRONMENT:
- Browser: Chrome / Firefox / Safari / Edge
- Device: Windows / Mac / Linux
- OS Version: [Version]
- Internet: Fast / Slow / Spotty

ATTACHMENTS:
- Screenshot of error
- Debug page screenshot
- Browser console log (F12 → Console)
```

**Step 3: Send to Support**

**Email Template:**
```
TO: technical-support@company.com
SUBJECT: [BUG] Logistics Assistant Error - [Date] - [Error Type]

[Issue report from Step 2]

IMPACT:
- User cannot complete searches
- Results are incorrect
- [Other impacts]

ATTACHMENTS:
- error_screenshot.png
- debug_screenshot.png
- logs.txt
```

**Step 4: Follow Up**

- Support team responds within **24 hours**
- Keep communication open
- Provide additional info if requested
- Test fix when deployed
- Confirm resolution

---

## 📞 Support Contacts

| Type | Email | Response Time |
|------|-------|---|
| App Down | it-support@company.com | 1 hour |
| Slow Performance | devops@company.com | 2 hours |
| Wrong Results | database@company.com | 4 hours |
| Feature Request | product@company.com | 1 week |

---

**Last Updated**: September 26, 2026  
**Version**: 1.0  
**Status**: Active & Maintained
