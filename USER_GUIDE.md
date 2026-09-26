# 👥 USER GUIDE - Logistics Compliance Assistant

**Version**: 1.0  
**Last Updated**: September 26, 2026  
**For**: Supply chain managers, compliance officers, logistics coordinators

---

## 📖 Table of Contents

1. [Getting Started](#getting-started)
2. [Features Overview](#features-overview)
3. [How to Use](#how-to-use)
4. [FAQ](#faq)
5. [Troubleshooting](#troubleshooting)
6. [Error Reporting](#error-reporting)

---

## 🚀 Getting Started

### Access the App

**Public URL**: `https://[username]-logistics-assistant.streamlit.app`

No installation needed! Just open the URL in any web browser:
- Chrome ✅
- Firefox ✅
- Safari ✅
- Edge ✅

### What You Need

- ✅ Internet connection
- ✅ Web browser
- ✅ Product IDs (from your company database)
- ✅ Country names (source and destination)

---

## ✨ Features Overview

### **1. Compliance Lookup** 🔍
Find import/export compliance requirements for any product shipment.

**What it does:**
- Looks up product information from database
- Searches for compliance requirements
- Shows duties, taxes, required documents
- Provides payment methods info

**Who needs it:** Logistics managers, customs brokers, supply chain planners

### **2. Product Search** 📦
Search for products in the database.

**Options:**
- Search by Product ID
- Search by Product Name
- Search by Category
- View all products

**Who needs it:** Warehouse staff, inventory managers

### **3. Debug Page** 🔧
Check app health and token usage.

**Info shown:**
- Database status
- API connection status
- Token usage statistics
- System information

**Who needs it:** Technical team, system administrators

### **4. About Page** ℹ️
Learn about the application and technology.

---

## 📋 How to Use

### **STEP 1: Compliance Lookup (Most Common)**

1. **Click "Compliance Lookup"** tab at top

2. **Enter Product ID**
   - Example: `P1001`
   - Check with your inventory team if unsure

3. **Enter Source Country**
   - Where product is shipped FROM
   - Example: `United States`

4. **Enter Destination Country**
   - Where product is shipped TO
   - Example: `India`

5. **Click "Get Compliance Info"**
   - ⏳ Wait 5-15 seconds for results
   - 🔄 App is thinking... be patient!

6. **Review Results**
   - Product details (name, category, HSN code)
   - Compliance requirements
   - Required documents
   - Duty information
   - Payment methods

---

### **STEP 2: Product Search**

1. **Click "Product Search"** tab

2. **Choose search method:**
   - **By ID**: Enter product code (P1001)
   - **By Name**: Enter product name (Electronics, Textiles)
   - **By Category**: Enter category (Electronics, Clothing)
   - **View All**: See all 500+ products

3. **Click "Search"**

4. **Review results** in table

---

### **STEP 3: Check System Health**

1. **Click "Debug"** tab (optional)

2. **View:**
   - ✅ Database: Connected/Disconnected
   - ✅ API: Working/Error
   - 📊 Token usage: Current consumption

3. **Screenshot for support** if issues arise

---

## ❓ FAQ

### **Q1: How long does a compliance search take?**
**A**: Typically 5-15 seconds. If longer:
- Check your internet connection
- Check if "Use ReAct Agent" toggle is enabled
- Try a different product ID

### **Q2: What if product ID is not found?**
**A**: 
- Check spelling and capitalization (case-sensitive)
- Use "Product Search" to find correct ID
- Contact your inventory team if product is missing from database

### **Q3: Can I search for multiple products at once?**
**A**: Not in this version. Search one product at a time.

### **Q4: What countries are supported?**
**A**: All countries. Enter official country names (e.g., "United States", "United Kingdom", "South Africa").

### **Q5: Is my data secure?**
**A**: Yes! 
- No personal data stored
- No login credentials saved
- Search history not recorded
- All data is processed securely

### **Q6: Can I export results?**
**A**: Copy-paste the results from the app. For bulk exports, contact technical team.

### **Q7: What if results seem incorrect?**
**A**: 
- Verify product ID is correct
- Check source/destination countries are spelled correctly
- Try another search
- Report to technical team (see Error Reporting below)

### **Q8: Is the app available 24/7?**
**A**: Yes! The app runs continuously. If you see errors, it's likely temporary. Refresh and try again.

### **Q9: Do I need special software or plugins?**
**A**: No! Just a modern web browser. No installations needed.

### **Q10: How often is the product database updated?**
**A**: Database has 500+ products. For updates, contact your database administrator.

---

## 🆘 Troubleshooting

### **Problem: "Groq API Key not found"**

**Cause**: API key not configured  
**Solution**: Contact your IT team. They need to add the key in Streamlit Cloud settings.

---

### **Problem: App takes too long (>30 seconds)**

**Cause**: Network issue or high load  
**Solutions**:
1. Check internet connection
2. Refresh the page (F5)
3. Disable "Use ReAct Agent" toggle for faster results
4. Try again in 5 minutes

---

### **Problem: "Product not found"**

**Cause**: Wrong product ID or spelling  
**Solutions**:
1. Use "Product Search" feature to find correct ID
2. Check for extra spaces: `P 1001` → `P1001`
3. Verify case: `p1001` → `P1001`

---

### **Problem: Results look wrong**

**Cause**: Incorrect source/destination countries  
**Solutions**:
1. Double-check country spelling
2. Use full country name: `USA` → `United States`
3. Try again with correct countries

---

### **Problem: "Something went wrong" error**

**Cause**: Technical issue  
**Solutions**:
1. Refresh the page (F5)
2. Wait 2-3 minutes
3. Try a different product
4. Report to technical team (see below)

---

### **Problem: Can't access the app**

**Cause**: Website down or network issue  
**Solutions**:
1. Check internet connection
2. Try different browser
3. Clear browser cache (Ctrl+Shift+Delete)
4. Wait 5 minutes and try again
5. Contact IT if persistent

---

## 📧 Error Reporting

### **When to Report**

Report errors if:
- ❌ App doesn't load
- ❌ Compliance search returns error
- ❌ Results seem incorrect
- ❌ App freezes (>2 minutes)
- ❌ Any unexpected behavior

### **How to Report**

**STEP 1: Gather Evidence**

- **Screenshot**: Press PrintScreen or Cmd+Shift+4 (Mac)
  - Capture the error message
  - Include the entire app screen

- **Error Message**: Write down the exact text (word-for-word)
  - Example: "Groq API Key not found"

- **When it happened**: Note the date and time
  - Example: "September 26, 2026, 3:45 PM"

- **What you did**: Steps you took before error
  - Example: "Entered P1001, USA, India"

- **Product ID & Countries**: Write down what you searched for
  - Example: "Product: P1001, From: USA, To: India"

### **STEP 2: Collect Information**

**Click the "Debug" tab and take a screenshot showing:**
- Database status ✅/❌
- API status ✅/❌
- Token usage numbers

### **STEP 3: Report to Technical Team**

**Email to**: `technical-support@company.com`  
**Subject**: `Logistics Assistant Error Report - [DATE] - [ERROR TYPE]`

**Email Content Template:**

```
ERROR REPORT
============

Date & Time: September 26, 2026, 3:45 PM
Error Type: Product Not Found / Slow Response / App Crash (choose one)

WHAT HAPPENED:
[Describe what you were trying to do]

STEPS TO REPRODUCE:
1. Click "Compliance Lookup"
2. Enter Product ID: P1001
3. Enter Source: United States
4. Click "Get Compliance Info"

ERROR MESSAGE:
[Copy exact error message here]

ATTACHMENTS:
- Screenshot of error (attached)
- Debug page screenshot (attached)

ADDITIONAL INFO:
- Browser: Chrome / Firefox / Safari / Edge
- Device: Windows / Mac / Linux
- Internet: Fast / Slow / Spotty

IMPACT:
- Cannot complete compliance searches
- Results are incorrect
- [Other impact description]
```

### **STEP 4: Follow Up**

- Technical team will investigate
- Expect response within 24 hours
- Do NOT reply to support email if investigating
- Support team will update you on progress

---

## 📞 Support Contacts

| Issue Type | Contact | Response Time |
|-----------|---------|---|
| App Down | IT Help Desk | 1 hour |
| Wrong Results | Database Team | 4 hours |
| Slow Performance | DevOps Team | 2 hours |
| Feature Request | Product Team | 1 week |

---

## 🎯 Quick Reference

| Task | Steps |
|------|-------|
| Find compliance requirements | Compliance Lookup → Enter ID/Countries → Get Info |
| Find product ID | Product Search → By Name → Search |
| Check app health | Debug tab → View status |
| Report error | Screenshot + Email to support team |
| Get API key issue fixed | Contact IT Help Desk |

---

## 💡 Tips for Best Results

✅ **Do:**
- Use correct product IDs from your system
- Use full country names (United States, not USA)
- Check your internet connection
- Refresh the page if something seems off
- Report errors with screenshots

❌ **Don't:**
- Don't make up product IDs
- Don't use abbreviations for countries
- Don't use special characters in searches
- Don't refresh too frequently (it restarts the search)
- Don't share the app URL with unauthorized users

---

## 📚 Additional Resources

- **Technical Docs**: For developers - [TECHNICAL_DOCS.md](TECHNICAL_DOCS.md)
- **Troubleshooting Guide**: Detailed fixes - [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **FAQ Extended**: More Q&A - See support team

---

**Last Updated**: September 26, 2026  
**Status**: Active & Maintained  
**Support**: contact technical-support@company.com
