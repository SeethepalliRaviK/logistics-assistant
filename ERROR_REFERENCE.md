# Error Reference Guide - Logistics Compliance Assistant

**Quick lookup guide for debugging common errors in the application.**

---

## 1. Database Connection Errors

### Error: `Product ID 'XXXX' not found in database`

**Root Cause:** The `get_product_by_id()` function in `core/database.py` was closing the connection before retrieving column names.

**Location:** `core/database.py:16-54`

**Solution Applied:**
```python
# ❌ WRONG - Connection closed before use
row = cursor.fetchone()
conn.close()  # Connection closed here
cursor = conn.cursor()  # Trying to use closed connection!

# ✅ CORRECT - Get columns first, then query
cursor.execute("PRAGMA table_info(products)")  # Get columns while connection open
columns = [col[1] for col in cursor.fetchall()]
# Then execute product query
row = cursor.fetchone()  # Fetch data while connection still open
conn.close()  # Close after all operations
return dict(zip(columns, row))
```

**Prevention:**
- Always fetch column names BEFORE closing the connection
- Keep connection open for entire operation
- Close connection only after all queries complete

**Quick Fix:**
1. Check `core/database.py` line 16-54
2. Ensure column retrieval happens before `conn.close()`
3. Verify data fetch happens while connection is open

---

## 2. Agent Configuration Errors

### Error: `create_react_agent() got unexpected keyword arguments`

**Root Causes:**
1. First attempt: Used `state_modifier=SYSTEM_PROMPT` (outdated parameter)
2. Second attempt: Used `system_prompt=SYSTEM_PROMPT` (not supported in this version)

**Location:** `core/agent.py:32-51`

**Solution Applied:**
```python
# ❌ WRONG - Direct parameter passing
agent_executor = create_react_agent(
    model=llm,
    tools=tools,
    state_modifier=SYSTEM_PROMPT,  # Not accepted
)

# ✅ CORRECT - Bind to model first
model_with_system = llm.bind(system=SYSTEM_PROMPT)
agent_executor = create_react_agent(
    model=model_with_system,
    tools=tools,
)
```

**Prevention:**
- Bind system prompts to the model using `.bind(system=...)`
- Don't pass system prompt directly to `create_react_agent()`
- Check LangChain/LangGraph version compatibility

**Quick Fix:**
1. Open `core/agent.py`
2. Use `model.bind(system=SYSTEM_PROMPT)` instead of direct parameter
3. Pass bound model to `create_react_agent()`

---

## 3. Tool Name Validation Errors

### Error: `tool 'Product Lookup' cannot contain whitespace in its name`

**Root Cause:** Tool names had spaces (e.g., "Product Lookup", "Web Search"), but Groq's API requires underscore or camelCase naming.

**Location:** `core/tools.py:101-128`

**Solution Applied:**
```python
# ❌ WRONG - Spaces in tool names
Tool(
    name="Product Lookup",  # Has space!
    func=product_lookup_tool,
)

# ✅ CORRECT - Underscores or camelCase
@tool
def product_lookup(product_id: str) -> str:
    """..."""
```

**Prevention:**
- Never use spaces in tool names
- Use snake_case (underscores) for tool names
- Use `@tool` decorator (automatically handles naming)

**Quick Fix:**
1. Search `core/tools.py` for spaces in tool names
2. Replace spaces with underscores: "Product Lookup" → "product_lookup"
3. Clear Streamlit cache: `rm -rf .streamlit/cache`
4. Restart Streamlit server

---

## 4. Tool Schema Validation Errors

### Error: `parameters for tool product_lookup did not match schema: errors: [missing properties: '__arg1']`

**Root Cause:** Using `Tool()` class constructor instead of `@tool` decorator. The Tool class doesn't automatically generate proper schema for single-argument functions.

**Location:** `core/tools.py:95-131`

**Solution Applied:**
```python
# ❌ WRONG - Manual Tool class
tools = {
    "product_lookup": Tool(
        name="product_lookup",
        func=product_lookup_tool,
        description="...",
    ),
}

# ✅ CORRECT - Use @tool decorator
from langchain_core.tools import tool

@tool
def product_lookup(product_id: str) -> str:
    """Look up product details from the database."""
    # Implementation
```

**Prevention:**
- Always use `@tool` decorator for tools
- Never manually instantiate `Tool()` class
- `@tool` automatically handles schema validation

**Quick Fix:**
1. Open `core/tools.py`
2. Replace `Tool()` instantiation with `@tool` decorator
3. Simplify `get_tools_list()` to return decorated functions
4. Clear cache and restart

---

## 5. Missing Required Tool Parameters

### Error: `parameters for tool compliance_search did not match schema: errors: [missing properties: 'source_country']`

**Root Cause:** Agent called `compliance_search()` with only `hs_code` and `destination_country`, but function required `source_country` as well.

**Location:** `core/tools.py:77-93` and `core/agent.py:128-132`

**Solution Applied:**
```python
# ❌ WRONG - Three required parameters
def compliance_search(hs_code: str, source_country: str, destination_country: str) -> str:
    # Agent can't always provide source_country context

# ✅ CORRECT - Only essential parameters
@tool
def compliance_search(hs_code: str, destination_country: str) -> str:
    """Search for compliance requirements based on HS code and destination country."""
    query = f"Import requirements for HS code {hs_code} to {destination_country}..."
    return web_search(query, max_results=5)
```

**Prevention:**
- Design tools with only essential, required parameters
- Make optional parameters have defaults
- Keep parameter count minimal for agent tools
- Test agent invocation with actual tools

**Quick Fix:**
1. Review tool function signatures
2. Remove non-essential parameters
3. Simplify parameter requirements
4. Update agent calls to match new signature

---

## 6. Agent Recursion Limit Exceeded

### Error: `Sorry, need more steps to process this request.`

**Root Cause:** `AGENT_RECURSION_LIMIT` was set to 12 steps, insufficient for complex multi-step agent reasoning.

**Location:** `core/__init__.py:14`

**Solution Applied:**
```python
# ❌ TOO LOW
AGENT_RECURSION_LIMIT = 12

# ✅ ADEQUATE for complex agents
AGENT_RECURSION_LIMIT = 30
```

**Why 30 steps?**
1. Agent thinks about task (1-2 steps)
2. Calls product_lookup tool (1 step)
3. Processes result (1 step)
4. Calls compliance_search tool (1 step)
5. Processes result (1 step)
6. Formats response (1 step)
7. Plus buffer for edge cases and retries (4-5 steps)
= Minimum ~15 steps, 30 provides safety margin

**Prevention:**
- Start with `AGENT_RECURSION_LIMIT = 25-30` for multi-step agents
- Increase if agent fails with "need more steps" error
- Monitor actual steps used via agent debugging

**Quick Fix:**
1. Open `core/__init__.py`
2. Change `AGENT_RECURSION_LIMIT` to 25-30
3. Clear cache: `rm -rf .streamlit/cache`
4. Restart Streamlit

---

## 7. Cache-Related Issues

### Symptoms:
- Changes to code don't appear in running app
- Old tool names still showing in errors
- Cached agent with outdated configuration

**Solution:**
```bash
# Clear Streamlit cache
rm -rf .streamlit/cache

# Then restart Streamlit server
# Press Ctrl+C to stop
# Run: streamlit run app.py
```

**Prevention:**
- Clear cache after every code change
- Restart Streamlit server after cache clear
- Don't just reload browser (Python modules stay cached)

---

## 8. Groq API Key Issues

### Error: `Groq API Key not found!`

**Solution:**
```toml
# Create .streamlit/secrets.toml
groq_api_key = "your-key-here"
```

**Add to .gitignore:**
```
.streamlit/secrets.toml
```

**Prevent exposure:**
- Never commit secrets.toml
- Use environment variables in production
- Store in platform-specific secrets (GitHub Secrets, Streamlit Cloud Secrets)

---

## Error Diagnosis Flowchart

```
Error in compliance lookup?
│
├─→ "Product not found in database"
│   └─→ Check: core/database.py line 16-54
│       └─→ Verify column retrieval before conn.close()
│
├─→ "create_react_agent() got unexpected keyword arguments"
│   └─→ Check: core/agent.py line 44-49
│       └─→ Use model.bind(system=...) instead
│
├─→ "tool cannot contain whitespace in its name"
│   └─→ Check: core/tools.py tool definitions
│       └─→ Use snake_case: "Product Lookup" → "product_lookup"
│       └─→ Use @tool decorator
│       └─→ Clear cache: rm -rf .streamlit/cache
│
├─→ "missing properties: '__arg1'"
│   └─→ Check: core/tools.py
│       └─→ Replace Tool() with @tool decorator
│       └─→ Clear cache
│
├─→ "missing properties: 'source_country'"
│   └─→ Check: Tool function signatures
│       └─→ Remove non-essential parameters
│       └─→ Update agent calls
│       └─→ Clear cache
│
├─→ "need more steps to process this request"
│   └─→ Check: core/__init__.py
│       └─→ Increase AGENT_RECURSION_LIMIT to 25-30
│       └─→ Clear cache
│
└─→ "Code changes not appearing"
    └─→ Clear cache: rm -rf .streamlit/cache
    └─→ Restart Streamlit (Ctrl+C, then streamlit run app.py)
```

---

## Testing Checklist After Changes

- [ ] Clear Streamlit cache: `rm -rf .streamlit/cache`
- [ ] Restart Streamlit server
- [ ] Test with Product ID: P1002
- [ ] Source Country: India
- [ ] Destination Country: USA
- [ ] Check for errors in Streamlit UI
- [ ] Verify product information displays correctly
- [ ] Verify compliance requirements are fetched
- [ ] Check token usage is within limits
- [ ] Verify no console errors

---

## Files to Check for Different Error Types

| Error Type | Primary File | Secondary Files |
|-----------|-------------|-----------------|
| Database lookup fails | `core/database.py` | `app.py` line 220 |
| Agent creation fails | `core/agent.py` | `core/__init__.py` |
| Tool validation fails | `core/tools.py` | `core/agent.py` |
| Tool parameter mismatch | `core/tools.py` | `core/agent.py` |
| Recursion limit exceeded | `core/__init__.py` | `app.py` line 77 |
| Cache issues | `.streamlit/cache/` | (clear entire dir) |
| API key missing | `.streamlit/secrets.toml` | `app.py` line 75-90 |

---

## Additional Resources

- **LangChain Docs:** https://python.langchain.com
- **LangGraph Docs:** https://langchain-ai.github.io/langgraph/
- **Groq API Docs:** https://console.groq.com/docs
- **Streamlit Docs:** https://docs.streamlit.io

