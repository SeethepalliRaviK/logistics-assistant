# 🧪 Testing Guide

## Test Coverage

**Current Status**: ✅ 80/80 unit tests passing

### Test Files

1. **test_database.py** (11 tests)
   - SQLite database operations
   - Product lookup and search
   - Query execution and security
   - Error handling and resilience

2. **test_groq_client.py** (23 tests)
   - Token budget tracking
   - Token estimation
   - Rate limit detection
   - Retry-after parsing
   - Edge cases with Unicode/special characters

3. **test_helpers.py** (26 tests)
   - Text clipping and whitespace handling
   - Input validation (Product ID, Country)
   - Product display formatting
   - Safe display with truncation

4. **test_app_structure.py** (20 tests)
   - File and directory structure
   - Module imports
   - Configuration validation
   - Database existence

## Running Tests

### Unit Tests (No API Key Required)

```bash
# Run all unit tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_database.py -v

# Run with coverage
python -m pytest tests/ --cov=core --cov=utils --cov-report=term-missing

# Run quickly (just pass/fail)
python -m pytest tests/ -q
```

### Integration Tests (Requires Groq API Key)

**Before running integration tests, set your Groq API key:**

#### Windows:
```bash
set GROQ_API_KEY=gsk_your_actual_key_here
python -m pytest tests/test_groq_integration.py -v
```

#### macOS/Linux:
```bash
export GROQ_API_KEY=gsk_your_actual_key_here
python -m pytest tests/test_groq_integration.py -v
```

### Full Test Suite

```bash
# Run everything (will skip Groq tests if no API key)
python -m pytest tests/ -v --tb=short

# Show test summary
python -m pytest tests/ --tb=no -q
```

## Integration Testing Checklist

Once you provide your Groq API key, verify:

- [ ] **Groq API Connection**
  - LLM can be created with API key
  - Can invoke simple LLM calls

- [ ] **Product Lookup**
  - Database products can be retrieved
  - Product data is accessible

- [ ] **Compliance Lookup**
  - Simple compliance lookup (no agent) works
  - Results are non-empty
  - Response handling is correct

- [ ] **Rate Limiting**
  - Token budget tracking works
  - No unexpected throttling

- [ ] **Error Handling**
  - Invalid API keys are rejected
  - Empty keys are rejected
  - Failures are handled gracefully

## Testing the Streamlit App

### Test Locally Before GitHub

1. **Set up secrets file:**
   ```bash
   mkdir -p .streamlit
   echo 'groq_api_key = "gsk_your_key"' > .streamlit/secrets.toml
   ```

2. **Run the app:**
   ```bash
   streamlit run app.py
   ```

3. **Test in browser** (http://localhost:8501):
   - [ ] Page loads without errors
   - [ ] Sidebar menu works
   - [ ] Can view debug page
   - [ ] Can search products
   - [ ] Can enter compliance query
   - [ ] Can toggle "Use ReAct Agent" setting
   - [ ] Get compliance results
   - [ ] View token usage stats

### Test Pages

**1. Compliance Lookup**
- Enter Product ID: `P001` (or valid ID from database)
- Enter Source Country: `United States`
- Enter Destination Country: `India`
- Click "Get Compliance Info"
- Verify product info is shown
- Verify compliance requirements appear

**2. Product Search**
- Try each search method:
  - By Product ID
  - By Product Name
  - By Category
  - View All Products
- Verify results display correctly

**3. About Page**
- Verify page loads and displays correctly
- Check all links are present

**4. Debug Page**
- Verify database status shows correct info
- Check API status
- Review token usage

## Test Coverage Report

```bash
# Generate coverage report
python -m pytest tests/ --cov=core --cov=utils --cov-report=html

# View report
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
```

## Automated Testing (GitHub Actions)

When you push to GitHub, the workflow will:

1. ✅ Run all unit tests
2. ✅ Check for linting issues
3. ✅ Verify imports
4. ✅ Check database exists
5. ✅ Run security scan
6. ✅ Show test results

**Note**: Groq API tests are skipped in CI (no API key in GitHub Actions).

## Performance Testing

### Test Response Times

```bash
# Time the compliance lookup
time python -c "
from core.database import get_all_products
from core.agent import simple_compliance_lookup
import os

products = get_all_products(limit=1)
if products:
    pid = products[0].get('product_id')
    result = simple_compliance_lookup(
        os.environ.get('GROQ_API_KEY'),
        pid, 'USA', 'India'
    )
    print(f'Response: {len(result)} chars')
"
```

## Troubleshooting

### Tests Fail with "Database closed"
- The database connection issue is handled gracefully
- Tests will skip instead of failing

### Groq API Tests Skipped
- Set the `GROQ_API_KEY` environment variable
- Use `export` on macOS/Linux
- Use `set` on Windows

### ImportError on Streamlit
- Run: `pip install -r requirements.txt`
- Verify Streamlit is installed: `python -c "import streamlit; print(streamlit.__version__)"`

### Streamlit Secrets Not Found
- Create `.streamlit/secrets.toml`:
  ```
  mkdir -p .streamlit
  echo 'groq_api_key = "your_key"' > .streamlit/secrets.toml
  ```
- Verify it's in `.gitignore`

## Next Steps

1. **Provide your Groq API key** (via private message or safely)
2. **Run integration tests** to verify Groq connection
3. **Test the Streamlit app locally**
4. **Commit final changes**
5. **Push to GitHub**
6. **Deploy to Streamlit Cloud**

---

**Test Status**: Ready for integration testing with your Groq API key! 🚀
