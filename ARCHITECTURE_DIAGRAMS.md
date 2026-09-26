# 🏗️ ARCHITECTURE & PROCESS FLOW DIAGRAMS

**Version**: 1.0  
**Last Updated**: September 26, 2026  
**For**: All technical stakeholders

---

## 📖 Table of Contents

1. [System Architecture](#system-architecture)
2. [Data Flow Diagram](#data-flow-diagram)
3. [Compliance Lookup Process](#compliance-lookup-process)
4. [Rate Limiting Logic](#rate-limiting-logic)
5. [Deployment Pipeline](#deployment-pipeline)
6. [Error Handling Flow](#error-handling-flow)
7. [Component Interactions](#component-interactions)

---

## 🏗️ System Architecture

### **High-Level System Architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                            │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │    Streamlit Web Interface (HTML/CSS/JavaScript)         │  │
│  │  ┌────────────┐  ┌────────────┐  ┌──────────────┐        │  │
│  │  │Compliance  │  │  Product   │  │   Debug      │        │  │
│  │  │  Lookup    │  │   Search   │  │   Page       │        │  │
│  │  └────────────┘  └────────────┘  └──────────────┘        │  │
│  │         │               │               │                  │  │
│  │         └───────────┬───┴───────────────┘                  │  │
│  │                     │                                       │  │
│  │             Input Validation                              │  │
│  │             (Product ID, Country)                         │  │
│  └──────────────────────┬──────────────────────────────────┘  │
└─────────────────────────┼────────────────────────────────────┘
                          │ HTTP POST
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   STREAMLIT CLOUD (Python)                      │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │              Core Application Logic (app.py)             │ │
│  │                                                          │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐ │ │
│  │  │ Input        │  │ Business     │  │ Output        │ │ │
│  │  │ Processing   │→ │ Logic        │→ │ Formatting    │ │ │
│  │  │ (validate)   │  │ (core/)      │  │ (display)     │ │ │
│  │  └──────────────┘  └──────────────┘  └───────────────┘ │ │
│  │                                                          │ │
│  └────────────────────┬─────────────────────────────────────┘ │
│                       │                                        │
│  ┌────────────────────┼─────────────────────────────────────┐ │
│  │                    │ Core Modules                        │ │
│  │  ┌─────────────────┴──────────┬──────────────┐          │ │
│  │  │                            │              │           │ │
│  │  ▼                            ▼              ▼           │ │
│  │  ┌─────────────────┐  ┌──────────────┐  ┌─────────────┐ │ │
│  │  │ groq_client.py  │  │ database.py  │  │  tools.py   │ │ │
│  │  │                 │  │              │  │             │ │ │
│  │  │ • TokenBudget   │  │ • SQLite ORM │  │ • Products  │ │ │
│  │  │ • Rate Limiting │  │ • Queries    │  │ • Web Search│ │ │
│  │  │ • LLM Instance  │  │ • Connection │  │ • Tools     │ │ │
│  │  └────────┬────────┘  └──────┬───────┘  └────┬────────┘ │ │
│  │           │                  │               │            │ │
│  │           └──────────────────┼───────────────┘            │ │
│  │                              │                            │ │
│  │  ┌──────────────────────────┴──────────────┐              │ │
│  │  │       agent.py (ReAct Agent)           │              │ │
│  │  │  • Reasoning loop                      │              │ │
│  │  │  • Tool selection & invocation         │              │ │
│  │  │  • Response generation                 │              │ │
│  │  └──────────────────────────────────────────┘              │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                       │      │      │                            │
│  ┌────────────────────┴──────┼──────┴────────────────────────┐   │
│  │         External Connections                             │   │
│  │                    │      │      │                        │   │
│  └────────────────────┼──────┼──────┼────────────────────────┘   │
└───────────────────────┼──────┼──────┼────────────────────────────┘
                        │      │      │
        ┌───────────────┼──────┼──────┼───────────────┐
        │               │      │      │               │
        ▼               ▼      ▼      ▼               ▼
   ┌─────────┐   ┌─────────────┐  ┌──────────┐  ┌─────────────┐
   │  Groq   │   │   SQLite    │  │ DuckDuck │  │ Streamlit   │
   │   API   │   │  Database   │  │   Go     │  │   Secrets   │
   │         │   │             │  │          │  │ & Caching   │
   │External │   │ data/       │  │ External │  │             │
   │LLM      │   │ greatglobe  │  │  Search  │  │ (Encrypted) │
   │Service  │   │   .db       │  │          │  │             │
   └─────────┘   └─────────────┘  └──────────┘  └─────────────┘
```

---

## 📊 Data Flow Diagram

### **End-to-End Data Flow for Compliance Lookup**

```
┌─────────────────────────────────────────────────────────────────┐
│ INPUT LAYER - User provides data                               │
│                                                                 │
│  Product ID: "P1001"                                           │
│  Source Country: "United States"                               │
│  Destination Country: "India"                                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ VALIDATION LAYER - Check input correctness                     │
│                                                                 │
│  ✓ Product ID format: "P" + numbers                           │
│  ✓ Country names: Recognized countries                         │
│  ✓ Max lengths: ID < 50 chars, Country < 100 chars           │
│                                                                 │
│  Result: Valid ✅                                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ RATE LIMIT CHECK - Verify token budget                         │
│                                                                 │
│  Tokens used (60s window): 3,200 / 6,400                       │
│  Available: 3,200 tokens                                        │
│  Needed: ~500 tokens                                           │
│  Status: ✓ Can proceed                                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ DATABASE LOOKUP - Get product info                             │
│                                                                 │
│  Query: SELECT * FROM products WHERE product_id='P1001'       │
│                                                                 │
│  Result:                                                        │
│  {                                                              │
│    'product_id': 'P1001',                                      │
│    'name': 'Electronics Module',                               │
│    'category': 'Electronics',                                  │
│    'hsn_code': '8471.30',                                      │
│    'unit_price': 150.00                                        │
│  }                                                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ AGENT REASONING - Use LLM to find compliance info              │
│                                                                 │
│  Query: "Find import/export compliance for Electronics Module  │
│           from United States to India"                         │
│                                                                 │
│  Agent Steps:                                                   │
│  1. Use product_lookup_tool → Already have product info       │
│  2. Use web_search_tool → Search "HS code 8471.30 India       │
│                            import duty"                        │
│  3. Combine results → Generate compliance report              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ RESPONSE GENERATION - Format for display                       │
│                                                                 │
│  Result: Compliance report with:                               │
│  • Duty percentage                                              │
│  • Required documents                                           │
│  • Payment methods                                              │
│  • Restrictions                                                 │
│  • Processing time estimates                                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│ OUTPUT LAYER - Display to user                                 │
│                                                                 │
│  Streamlit UI shows:                                            │
│  ✓ Product details                                             │
│  ✓ Compliance requirements                                     │
│  ✓ Visual formatting                                           │
│  ✓ Token usage stats                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Compliance Lookup Process

### **Detailed Process Flow for User Query**

```
START: User enters data
        │
        ▼
    ┌─────────────────────────┐
    │ User clicks             │
    │ "Get Compliance Info"   │
    └──────────┬──────────────┘
               │
               ▼
    ┌─────────────────────────────────────┐
    │ app.py receives input               │
    │ • Product ID: P1001                 │
    │ • Source: United States             │
    │ • Destination: India                │
    └──────────┬──────────────────────────┘
               │
               ▼
    ┌────────────────────────────────────────────┐
    │ Input Validation (helpers.py)              │
    │ validate_product_id(P1001) → ✓ Valid      │
    │ validate_country(United States) → ✓ Valid │
    │ validate_country(India) → ✓ Valid         │
    └──────────┬─────────────────────────────────┘
               │
        Invalid?
        │      │
       No     Yes
        │      │
        │      ▼
        │   st.error("Invalid input")
        │   STOP
        │
        ▼
    ┌────────────────────────────────────────┐
    │ Check Rate Limit (groq_client.py)     │
    │                                        │
    │ TokenBudget.used() → 3200/6400        │
    │ Can spend 500? → YES ✓                │
    └──────────┬─────────────────────────────┘
               │
         Budget OK?
        │        │
      Yes       No
        │        │
        │        ▼
        │   time.sleep(60)  ← Wait for window
        │   Retry...
        │
        ▼
    ┌──────────────────────────────────┐
    │ Get Product from Database        │
    │ (database.py)                    │
    │                                  │
    │ product = get_product_by_id()   │
    └──────────┬───────────────────────┘
               │
         Product found?
        │              │
      Yes             No
        │              │
        │              ▼
        │          st.warning("Not found")
        │          STOP
        │
        ▼
    ┌──────────────────────────────────┐
    │ Check: Use Agent?                │
    │ (user toggle)                    │
    │                                  │
    │ use_agent = st.checkbox(...)     │
    └──────────┬───────────────────────┘
               │
        Agent enabled?
        │           │
       Yes         No
        │           │
        │           ▼
        │       ┌─────────────────────────────────┐
        │       │ Direct Lookup (FAST)            │
        │       │                                 │
        │       │ product_dict + web_search()    │
        │       │ → Compliance info              │
        │       │                                 │
        │       │ Time: 5-10 seconds             │
        │       └────────────┬────────────────────┘
        │                    │
        ▼                    │
    ┌──────────────────────┐ │
    │ Agent Mode (FULL)    │ │
    │                      │ │
    │ create_compliance_   │ │
    │ agent(api_key) →    │ │
    │                      │ │
    │ ReAct reasoning:     │ │
    │ 1. Plan steps       │ │
    │ 2. Call tools       │ │
    │ 3. Observe results  │ │
    │ 4. Generate answer  │ │
    │                      │ │
    │ Time: 10-20s        │ │
    └────────┬────────────┘ │
             │              │
             └──────────┬───┘
                        │
                        ▼
    ┌────────────────────────────────────┐
    │ Format Results (app.py)             │
    │                                     │
    │ format_product_display()           │
    │ format_compliance_results()        │
    └────────────┬─────────────────────────┘
                 │
                 ▼
    ┌──────────────────────────────────────┐
    │ Update Token Budget                  │
    │                                      │
    │ BUDGET.add_tokens(actual_tokens)    │
    │ Display usage: 3700/6400            │
    └────────────┬───────────────────────────┘
                 │
                 ▼
    ┌─────────────────────────────────────────┐
    │ Display Results to User                 │
    │ ✓ Product Details                       │
    │ ✓ Compliance Requirements               │
    │ ✓ Duty Information                      │
    │ ✓ Required Documents                    │
    │ ✓ Token Usage Stats                     │
    └─────────────────────────────────────────┘
                 │
                 ▼
           END: Success ✓
```

---

## ⏱️ Rate Limiting Logic

### **Token Budget Management (60-second Rolling Window)**

```
TIME ──────────────────────────────────────────────────────────────→

0s  ┌─────────────────────────────────────────────────────────────┐
    │ REQUEST 1: 500 tokens                                       │
    │ Window: [0, 60) seconds                                     │
    │ Used: 500 / 6400                                            │
    │ Available: 5900                                             │
    └─────────────────────────────────────────────────────────────┘

15s ┌─────────────────────────────────────────────────────────────┐
    │ REQUEST 2: 600 tokens                                       │
    │ Window: [0, 60) seconds                                     │
    │ Used: 500 + 600 = 1100 / 6400                              │
    │ Available: 5300                                             │
    └─────────────────────────────────────────────────────────────┘

30s ┌─────────────────────────────────────────────────────────────┐
    │ REQUEST 3: 5500 tokens (large query)                        │
    │ Check budget: 5300 available < 5500 needed?                │
    │ ACTION: WAIT 60 seconds before attempting                  │
    │                                                              │
    │ Meanwhile, time passes...                                   │
    └─────────────────────────────────────────────────────────────┘

60s ┌─────────────────────────────────────────────────────────────┐
    │ First request from 0s EXPIRES from window                   │
    │ Window: [60, 120) seconds                                   │
    │ Used: 600 (only request at 15s left)                       │
    │ Available: 5800                                             │
    │ ACTION: NOW can process REQUEST 3 (5500 tokens)            │
    │ Process REQUEST 3: 600 + 5500 = 6100 / 6400 ✓             │
    └─────────────────────────────────────────────────────────────┘

120s ┌────────────────────────────────────────────────────────────┐
     │ Request at 15s EXPIRES from window                        │
     │ Window: [120, 180) seconds                                │
     │ Used: 5500 (only request at 30s left)                    │
     │ Available: 900                                            │
     └────────────────────────────────────────────────────────────┘
```

### **Algorithm Pseudocode**

```python
class TokenBudget:
    def __init__(max_tokens=6400, window=60):
        self.token_log = []  # [(timestamp, tokens), ...]
    
    def used(self):
        """Calculate tokens used in current window"""
        now = time.time()
        cutoff = now - self.window
        
        # Keep only recent entries
        self.token_log = [
            (t, c) for t, c in self.token_log 
            if t > cutoff
        ]
        
        # Sum all tokens in window
        return sum(tokens for _, tokens in self.token_log)
    
    def can_spend(tokens):
        """Check if we have enough budget"""
        return self.used() + tokens <= self.max_tokens
    
    def reserve(tokens):
        """Wait if needed, then reserve tokens"""
        while not self.can_spend(tokens):
            sleep_time = self.wait_until_free()
            time.sleep(sleep_time)
            self.cleanup_old_entries()
    
    def add_tokens(tokens):
        """Record tokens used"""
        self.token_log.append((time.time(), tokens))
```

---

## 📦 Deployment Pipeline

### **GitHub → Streamlit Cloud Deployment Flow**

```
┌─────────────────────────────────────────────────────────────┐
│ DEVELOPER: Local Development                               │
│ ┌───────────────────────────────────────────────────────┐  │
│ │ 1. Edit code locally                                 │  │
│ │ 2. Run tests: pytest tests/ -v                       │  │
│ │ 3. Test app: streamlit run app.py                   │  │
│ │ 4. Commit: git commit -m "message"                  │  │
│ │ 5. Push: git push origin main                       │  │
│ └───────────┬───────────────────────────────────────────┘  │
└──────────────┼──────────────────────────────────────────────┘
               │ (git push)
               ▼
┌─────────────────────────────────────────────────────────────┐
│ GITHUB: Repository & Actions                              │
│ ┌───────────────────────────────────────────────────────┐  │
│ │ 1. Receive push on 'main' branch                    │  │
│ │ 2. Trigger GitHub Actions workflow                 │  │
│ │ 3. Setup Python 3.11 environment                   │  │
│ │ 4. Install dependencies: pip install -r ...        │  │
│ │                                                      │  │
│ │ AUTOMATED TESTS:                                    │  │
│ │ ├─ Run unit tests: pytest tests/ -q               │  │
│ │ ├─ Code quality: flake8 check                      │  │
│ │ ├─ Security scan: bandit                           │  │
│ │ ├─ File verify: Check structure                    │  │
│ │ │                                                    │  │
│ │ Test Results:                                       │  │
│ │ ✓ 87 tests pass                                    │  │
│ │ ✓ No security issues                              │  │
│ │ ✓ All files present                               │  │
│ │                                                      │  │
│ │ 5. Notify deployment ready                         │  │
│ └───────────┬───────────────────────────────────────────┘  │
└──────────────┼──────────────────────────────────────────────┘
               │ (webhook trigger)
               ▼
┌─────────────────────────────────────────────────────────────┐
│ STREAMLIT CLOUD: Build & Deploy                           │
│ ┌───────────────────────────────────────────────────────┐  │
│ │ Build Phase (2-3 minutes):                          │  │
│ │ 1. Allocate cloud resources                         │  │
│ │ 2. Clone repository                                 │  │
│ │ 3. Install Python 3.11.9 runtime                   │  │
│ │ 4. Install dependencies (requirements.txt)          │  │
│ │ 5. Prepare Streamlit environment                   │  │
│ │                                                      │  │
│ │ Start Phase (1-2 minutes):                         │  │
│ │ 6. Start Streamlit server                          │  │
│ │ 7. Load app.py                                     │  │
│ │ 8. Initialize cache & session state                │  │
│ │ 9. Health check - verify responsive               │  │
│ │                                                      │  │
│ │ Status: ✓ Running                                  │  │
│ └───────────┬───────────────────────────────────────────┘  │
└──────────────┼──────────────────────────────────────────────┘
               │ (app ready)
               ▼
┌─────────────────────────────────────────────────────────────┐
│ PRODUCTION: Live App                                        │
│ ┌───────────────────────────────────────────────────────┐  │
│ │ App URL: https://[username]-app.streamlit.app       │  │
│ │                                                      │  │
│ │ Features:                                            │  │
│ │ ✓ Auto-scaling                                      │  │
│ │ ✓ HTTPS/SSL                                         │  │
│ │ ✓ Global CDN                                        │  │
│ │ ✓ 99.5% uptime SLA                                 │  │
│ │ ✓ Automatic restarts                               │  │
│ │                                                      │  │
│ │ Monitoring:                                          │  │
│ │ ✓ Logs available in dashboard                      │  │
│ │ ✓ Error tracking enabled                           │  │
│ │ ✓ Performance metrics                              │  │
│ └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

TOTAL TIME: 5-10 minutes from push to live
```

---

## ❌ Error Handling Flow

### **Error Detection and Resolution Process**

```
┌─────────────────────────────┐
│ ERROR OCCURS               │
│ (In any component)          │
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│ ERROR CLASSIFICATION                        │
│                                             │
│ Type 1: Input Validation Error            │
│ Type 2: Database Error                    │
│ Type 3: API Error                         │
│ Type 4: Rate Limit Error                  │
│ Type 5: Network Error                     │
│ Type 6: Unknown Error                     │
└────────────┬────────────────────────────────┘
             │
    ┌────────┼────────┬────────┬────────┬────────┐
    │        │        │        │        │        │
    ▼        ▼        ▼        ▼        ▼        ▼
   Type1   Type2    Type3    Type4    Type5    Type6
    │        │        │        │        │        │
    ▼        ▼        ▼        ▼        ▼        ▼
┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐
│Display │  │Retry │ │Check  │ │Wait   │ │Retry  │ │Log    │
│User    │  │Query │ │API    │ │60s    │ │with   │ │Error  │
│Error   │  │      │ │Status │ │       │ │Backoff│ │Alert  │
│Message │  │      │ │       │ │       │ │       │ │       │
└────────┘  └────────┘└────────┘└────────┘└────────┘└────────┘
    │        │        │        │        │        │
    └────────┴────────┴────────┴────────┴────────┘
             │
             ▼
    ┌─────────────────────────┐
    │ Retry Logic             │
    │                         │
    │ Attempt 1: Immediately │
    │ Attempt 2: +5 second   │
    │ Attempt 3: +30 second  │
    │ Attempt 4: +60 second  │
    │ Max Attempts: 4        │
    └────────┬────────────────┘
             │
     Succeeded?
    │         │
   Yes       No
    │         │
    │         ▼
    │    ┌──────────────────┐
    │    │ Report Error to │
    │    │ User & Support   │
    │    └──────────────────┘
    │         │
    └─────────┴────────────────►
             │
             ▼
    ┌──────────────────────────┐
    │ Log Error Details:       │
    │ • Error message          │
    │ • Stack trace            │
    │ • User input             │
    │ • Timestamp              │
    │ • System state           │
    └────────┬─────────────────┘
             │
             ▼
    ┌──────────────────────────┐
    │ ALERT SYSTEM (if severe) │
    │ • Send to admin           │
    │ • Create support ticket   │
    │ • Page on-call if critical│
    └──────────────────────────┘
```

---

## 🔌 Component Interactions

### **Message Flow Diagram**

```
USER INTERFACE (Streamlit)
     │
     │ "Get Compliance Info"
     ▼
app.py (Main Controller)
     │
     ├─→ helpers.validate_product_id()
     │        │
     │        ▼
     │    utils/helpers.py
     │        │
     │        ▼ (valid/invalid)
     │
     ├─→ groq_client.TokenBudget.can_spend()
     │        │
     │        ▼
     │    core/groq_client.py
     │        │
     │        ├─→ (if can't spend: wait)
     │        │
     │        ▼ (can spend)
     │
     ├─→ database.get_product_by_id()
     │        │
     │        ▼
     │    core/database.py
     │        │
     │        ├─→ SQLite Connection
     │        │        │
     │        │        ▼
     │        │    data/greatglobe.db
     │        │
     │        ▼ (product dict)
     │
     ├─→ agent.invoke_agent() OR simple_compliance_lookup()
     │        │
     │        ├─→ agent.py / create_compliance_agent()
     │        │        │
     │        │        ├─→ create_llm()
     │        │        │        │
     │        │        │        ▼
     │        │        │    groq_client.RateLimitedChatGroq
     │        │        │        │
     │        │        │        ▼
     │        │        │    Groq API (External)
     │        │        │
     │        │        ├─→ tools.py (product_lookup_tool)
     │        │        │        │
     │        │        │        ▼
     │        │        │    database.search_products()
     │        │        │
     │        │        ├─→ tools.py (web_search_tool)
     │        │        │        │
     │        │        │        ▼
     │        │        │    duckduckgo_search.DDGS()
     │        │        │        │
     │        │        │        ▼
     │        │        │    DuckDuckGo API (External)
     │        │        │
     │        │        ▼ (reasoning result)
     │        │
     │        ▼
     │    Compliance Report
     │
     ├─→ groq_client.TokenBudget.add_tokens()
     │        │
     │        ▼
     │    Update token usage
     │
     ├─→ format results
     │        │
     │        ▼
     │    helpers.format_product_display()
     │    helpers.format_compliance_results()
     │
     ▼
Streamlit UI (Display Results)
     │
     ▼
USER SEES RESULTS
```

---

## 📈 Performance Characteristics

### **Typical Response Times**

```
Operation                          Typical    Max      Bottleneck
─────────────────────────────────────────────────────────────────
Input validation                   <10ms      50ms     Validation rules
Database product lookup            50-100ms   500ms    DB file I/O
Rate limit check                   <5ms       50ms     Token counting
Direct compliance lookup            5-10s      15s      API response
Full agent lookup                  10-20s     60s      Agent reasoning
Web search (DDGS)                  2-5s       10s      Network latency
LLM inference                      5-15s      30s      API processing

TOTAL (direct)                     5-15s      20s      API + DB
TOTAL (with agent)                10-25s     70s      Agent reasoning
────────────────────────────────────────────────────────────────────
```

---

**Last Updated**: September 26, 2026  
**Status**: Complete & Verified
