"""Core modules for Groq-powered logistics assistant."""

# Token budget controls
TPM_LIMIT = 8000
TPM_SAFETY = 0.80
RATE_RETRIES = 6

# Token budget controls for queries
MAX_INTERESTS = 2
MAX_RESULTS_PER_QUERY = 5
MAX_BODY_CHARS = 700
MAX_RESULTS_TO_FILTER = 8
MAX_URLS_TO_SUMMARIZE = 5
AGENT_RECURSION_LIMIT = 30
LLM_MAX_TOKENS = 2000

# Model configuration
MODEL_NAME = "openai/gpt-oss-120b"
USE_AGENT = True
