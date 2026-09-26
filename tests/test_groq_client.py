"""Unit tests for Groq client module."""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.groq_client import (
    TokenBudget,
    estimate_tokens,
    estimate_messages_tokens,
    parse_retry_after,
    is_rate_limit,
)


class TestTokenBudget(unittest.TestCase):
    """Test token budget tracking."""

    def setUp(self):
        """Set up test fixtures."""
        self.budget = TokenBudget(tpm_limit=1000, safety=0.8)

    def test_budget_initialization(self):
        """Test budget initializes with correct limit."""
        self.assertEqual(self.budget.limit, 800)  # 1000 * 0.8

    def test_budget_used_empty(self):
        """Test used() returns 0 when no tokens spent."""
        self.assertEqual(self.budget.used(), 0)

    def test_budget_reserve_and_used(self):
        """Test reserving tokens updates used amount."""
        self.budget.reserve(100)
        self.assertEqual(self.budget.used(), 100)

    def test_budget_multiple_reserves(self):
        """Test multiple token reservations accumulate."""
        self.budget.reserve(100)
        self.budget.reserve(150)
        self.assertEqual(self.budget.used(), 250)

    def test_budget_settle(self):
        """Test settling actual usage vs estimate."""
        self.budget.reserve(100)
        self.budget.settle(estimated=100, actual=75)
        self.assertEqual(self.budget.used(), 75)

    def test_budget_penalize(self):
        """Test penalizing after rate limit error."""
        self.budget.penalise()  # Note: British spelling in source code
        # Should mark the full limit as used
        self.assertEqual(self.budget.used(), self.budget.limit)


class TestTokenEstimation(unittest.TestCase):
    """Test token estimation functions."""

    def test_estimate_tokens_empty(self):
        """Test estimating tokens for empty string."""
        tokens = estimate_tokens("")
        self.assertEqual(tokens, 1)  # min of 1

    def test_estimate_tokens_text(self):
        """Test estimating tokens for text."""
        text = "Hello world, this is a test."
        tokens = estimate_tokens(text)
        # 29 chars / 3 = ~9-10 tokens
        self.assertGreater(tokens, 0)
        self.assertLess(tokens, 20)

    def test_estimate_tokens_long_text(self):
        """Test estimating tokens for longer text."""
        text = "a" * 300  # 300 characters
        tokens = estimate_tokens(text)
        # 300 / 3 = 100
        self.assertGreater(tokens, 90)
        self.assertLess(tokens, 110)

    def test_estimate_tokens_numbers(self):
        """Test estimating tokens for numeric input."""
        tokens = estimate_tokens(12345)
        self.assertGreater(tokens, 0)


class TestRateLimitDetection(unittest.TestCase):
    """Test rate limit error detection."""

    def test_rate_limit_429(self):
        """Test detecting 429 error."""
        error = Exception("429 Too many requests")
        self.assertTrue(is_rate_limit(error))

    def test_rate_limit_message(self):
        """Test detecting rate limit in message."""
        error = Exception("Rate limit exceeded")
        self.assertTrue(is_rate_limit(error))

    def test_not_rate_limit(self):
        """Test non-rate-limit error."""
        error = Exception("Connection timeout")
        # Timeout is not a rate limit error
        self.assertFalse(is_rate_limit(error))

    def test_rate_limit_case_insensitive(self):
        """Test rate limit detection is case insensitive."""
        error = Exception("RATE_LIMIT")
        self.assertTrue(is_rate_limit(error))


class TestRetryAfterParsing(unittest.TestCase):
    """Test parsing retry-after from error messages."""

    def test_parse_retry_seconds(self):
        """Test parsing seconds from error message."""
        msg = "Please try again in 3.53s"
        wait = parse_retry_after(msg)
        # Should be ~5.53 (3.53 + 2.0)
        self.assertGreater(wait, 5)
        self.assertLess(wait, 6)

    def test_parse_retry_milliseconds(self):
        """Test parsing milliseconds."""
        msg = "Please try again in 500ms"
        wait = parse_retry_after(msg)
        # Should be ~2.5s (500ms/1000 + 2.0)
        self.assertGreater(wait, 2)
        self.assertLess(wait, 3)

    def test_parse_retry_default(self):
        """Test default wait time when parsing fails."""
        msg = "Some random error message"
        wait = parse_retry_after(msg, default=30.0)
        self.assertEqual(wait, 30.0)

    def test_parse_retry_minutes_seconds(self):
        """Test parsing minutes and seconds."""
        msg = "Please try again in 1m30s"
        wait = parse_retry_after(msg)
        # Should be ~92s (60 + 30 + 2)
        self.assertGreater(wait, 91)
        self.assertLess(wait, 93)


class TestTokenEstimationEdgeCases(unittest.TestCase):
    """Test edge cases in token estimation."""

    def test_estimate_none(self):
        """Test estimating tokens for None."""
        tokens = estimate_tokens(None)
        self.assertEqual(tokens, 1)

    def test_estimate_special_chars(self):
        """Test estimating with special characters."""
        text = "!@#$%^&*()"
        tokens = estimate_tokens(text)
        self.assertGreater(tokens, 0)

    def test_estimate_unicode(self):
        """Test estimating with unicode characters."""
        text = "Hello 世界 مرحبا"
        tokens = estimate_tokens(text)
        self.assertGreater(tokens, 0)


if __name__ == '__main__':
    unittest.main()
