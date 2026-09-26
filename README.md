# 🌍 Logistics Compliance Assistant

An intelligent supply chain compliance assistant powered by Groq API and LangChain. This application helps logistics managers quickly retrieve product compliance requirements (import/export documents, duties, payment methods) based on source and destination countries.

## Features

- **Product Database Lookup**: Query product details from SQLite database using Product ID
- **Intelligent Web Search**: Uses DuckDuckGo to fetch up-to-date compliance information
- **LangChain ReAct Agent**: Autonomous reasoning agent that combines product data with web search results
- **Rate-Limited API Calls**: Built-in token budget management for Groq's free tier
- **Streamlit UI**: Interactive web interface for easy access
- **GitHub Actions CI/CD**: Automated testing and deployment pipeline

## Technology Stack

- **LLM**: Groq API (openai/gpt-oss-120b)
- **Framework**: LangChain + LangGraph
- **Frontend**: Streamlit
- **Database**: SQLite (greatglobe.db)
- **Deployment**: Streamlit Cloud
- **CI/CD**: GitHub Actions

## Project Structure

```
.
├── app.py                      # Main Streamlit application
├── core/                       # Core business logic
│   ├── __init__.py            # Configuration constants
│   ├── groq_client.py         # Rate-limited LLM client
│   ├── database.py            # Database operations
│   ├── tools.py               # LangChain tools
│   └── agent.py               # Agent setup and execution
├── utils/                      # Utility functions
│   └── helpers.py             # Helper functions
├── data/
│   └── greatglobe.db          # SQLite database
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── .github/workflows/
│   └── deploy.yml             # CI/CD workflow
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Installation

### Prerequisites
- Python 3.10 or higher
- Groq API key (get free at https://console.groq.com)
- Git
- GitHub account (for deployment)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/logistics-assistant.git
   cd logistics-assistant
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Groq API key locally**
   ```bash
   mkdir -p .streamlit
   echo 'groq_api_key = "your-groq-api-key-here"' > .streamlit/secrets.toml
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

The app will open in your browser at `http://localhost:8501`

## Environment Variables

### Local Development
Create `.streamlit/secrets.toml`:
```toml
groq_api_key = "gsk_..."  # Your Groq API key
```

### Streamlit Cloud
Add via app dashboard:
1. Go to app settings (gear icon)
2. Secrets section
3. Add `groq_api_key = "gsk_..."`

### GitHub Actions
Add via repository settings:
1. Settings → Secrets and variables → Actions
2. New repository secret: `GROQ_API_KEY`

## Deployment

### Option 1: Streamlit Cloud (Recommended)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit: Convert notebook to Streamlit app"
   git push -u origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Click "New app"
   - Connect GitHub account
   - Select repository, branch (main), and file (app.py)

3. **Add API key**
   - In app settings, add `groq_api_key` to Secrets
   - App will restart and use the secret

4. **Share**
   - App is live at `https://your-username-app-name.streamlit.app`

### Option 2: GitHub Actions (Advanced)

The repository includes a GitHub Actions workflow (`.github/workflows/deploy.yml`) that:
- Runs on every push to main
- Installs dependencies
- Runs tests (if added)
- Deploys to Streamlit Cloud

## Usage

1. **Enter Product ID**: Input a valid Product ID from the database
2. **Specify Countries**: Select or enter source and destination countries
3. **Get Compliance Info**: Click the button to fetch:
   - Product details (name, HSN code, category)
   - Import/export requirements
   - Duty information
   - Payment obligations

## API Rate Limits

The application uses Groq's free tier with the following limits:
- **Token Per Minute (TPM)**: 8,000 (default)
- **Safety Margin**: 80% of limit (6,400 tokens)
- **Auto-retry**: Up to 6 attempts on rate limit

If you hit rate limits, the app will automatically wait and retry.

## Configuration

Edit `core/__init__.py` to adjust:

```python
TPM_LIMIT = 8000              # Tokens per minute limit
TPM_SAFETY = 0.80            # Safety margin percentage
MAX_INTERESTS = 2             # Product attributes to track
MAX_RESULTS_PER_QUERY = 5     # Web search results per query
AGENT_RECURSION_LIMIT = 12    # Max agent loop iterations
LLM_MAX_TOKENS = 2000         # Max response length
```

## Database

The application uses `data/greatglobe.db` (SQLite) with product information:

| Field | Description |
|-------|-------------|
| Product_ID | Unique product identifier |
| Product_Name | Name of the product |
| Category | Broad classification |
| HSN_Code | Harmonized System code for customs |

To add products:
```python
import sqlite3
conn = sqlite3.connect('data/greatglobe.db')
cursor = conn.cursor()
cursor.execute(
    "INSERT INTO products (product_id, name, category, hsn_code) VALUES (?, ?, ?, ?)",
    (123, 'Product Name', 'Category', 'HSN123')
)
conn.commit()
```

## Troubleshooting

### "GROQ_API_KEY not set"
- Ensure the API key is in `.streamlit/secrets.toml` (local) or Streamlit Cloud settings
- Restart the app after adding the secret

### "Rate limit exceeded"
- The app will auto-retry. If you hit limits frequently, increase the `TPM_LIMIT` or decrease `MAX_RESULTS_PER_QUERY`

### "Product not found"
- Verify the Product ID exists in `data/greatglobe.db`
- Check the database connection in `core/database.py`

### Database connection errors
- Ensure `data/greatglobe.db` exists
- Check file permissions (read/write access)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

- **Groq API Docs**: https://console.groq.com/docs
- **LangChain Docs**: https://python.langchain.com
- **Streamlit Docs**: https://docs.streamlit.io
- **Issues**: Open an issue on GitHub

## Acknowledgments

- Built with [Groq](https://groq.com) - Speed is Freedom
- Powered by [LangChain](https://langchain.com)
- Deployed on [Streamlit Cloud](https://streamlit.io/cloud)

---

**Last Updated**: September 26, 2026
