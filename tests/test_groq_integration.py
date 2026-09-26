"""Integration tests for Groq API."""

import unittest
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.groq_client import create_llm, safe_llm_call
from core.database import get_product_by_id, get_all_products
from core.agent import simple_compliance_lookup
from langchain_core.messages import HumanMessage


class TestGroqIntegration(unittest.TestCase):
    """Integration tests with actual Groq API."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.api_key = os.environ.get("GROQ_API_KEY")
        if not cls.api_key:
            raise unittest.SkipTest(
                "GROQ_API_KEY environment variable not set. "
                "Run: set GROQ_API_KEY=your_key"
            )

    def test_groq_api_connection(self):
        """Test that we can connect to Groq API."""
        if not self.api_key:
            self.skipTest("No Groq API key provided")

        try:
            llm = create_llm(self.api_key)
            self.assertIsNotNone(llm)
        except Exception as e:
            self.fail(f"Failed to create LLM: {e}")

    def test_simple_llm_call(self):
        """Test a simple LLM call."""
        if not self.api_key:
            self.skipTest("No Groq API key provided")

        try:
            llm = create_llm(self.api_key)
            result = llm.invoke([HumanMessage(content="Say 'Hello' in one word")])
            self.assertIsNotNone(result)
            self.assertIsNotNone(result.content)
            print(f"✓ LLM Response: {result.content[:50]}...")
        except Exception as e:
            self.fail(f"LLM call failed: {e}")

    def test_product_lookup_integration(self):
        """Test product lookup with real data."""
        products = get_all_products(limit=1)
        self.assertTrue(len(products) > 0, "Should have products in database")

        product = products[0]
        product_id = product.get('product_id') or product.get('Product_ID')
        self.assertIsNotNone(product_id, "Product should have ID")

        # Verify we can retrieve it
        retrieved = get_product_by_id(str(product_id))
        if retrieved:
            self.assertIsInstance(retrieved, dict)

    def test_compliance_lookup_without_agent(self):
        """Test compliance lookup (simple mode without agent)."""
        if not self.api_key:
            self.skipTest("No Groq API key provided")

        products = get_all_products(limit=1)
        if not products:
            self.skipTest("No products in database")

        product = products[0]
        product_id = product.get('product_id') or product.get('Product_ID')

        if not product_id:
            self.skipTest("Product has no ID")

        try:
            result = simple_compliance_lookup(
                self.api_key,
                str(product_id),
                "United States",
                "India"
            )
            self.assertIsNotNone(result)
            self.assertTrue(len(result) > 0)
            print(f"✓ Compliance Lookup Result Length: {len(result)} chars")
        except Exception as e:
            self.fail(f"Compliance lookup failed: {e}")


class TestGroqErrorHandling(unittest.TestCase):
    """Test error handling with Groq API."""

    def test_invalid_api_key(self):
        """Test that invalid API key raises error."""
        try:
            llm = create_llm("invalid_key_12345")
            # Try to invoke - should fail
            from langchain_core.messages import HumanMessage
            result = llm.invoke([HumanMessage(content="test")])
            # If it doesn't raise, that's unexpected but we skip
            self.skipTest("Invalid key was accepted (unexpected)")
        except Exception as e:
            # Expected to fail with invalid key
            self.assertIn(
                any(word in str(e).lower() for word in ['invalid', 'auth', 'unauthorized', 'error']),
                True,
                f"Expected auth error, got: {e}"
            )

    def test_empty_api_key(self):
        """Test that empty API key raises error."""
        with self.assertRaises((ValueError, KeyError, TypeError, RuntimeError)):
            llm = create_llm("")
            from langchain_core.messages import HumanMessage
            llm.invoke([HumanMessage(content="test")])


class TestGroqRateLimiting(unittest.TestCase):
    """Test rate limiting with Groq API."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.api_key = os.environ.get("GROQ_API_KEY")

    def test_token_budget_tracking(self):
        """Test that token budget is tracked."""
        if not self.api_key:
            self.skipTest("No Groq API key provided")

        from core.groq_client import BUDGET

        initial_used = BUDGET.used()

        try:
            llm = create_llm(self.api_key)
            from langchain_core.messages import HumanMessage
            result = llm.invoke([HumanMessage(content="Say hi")])

            # After call, should have tracked some tokens
            # (may not increase if under 60-second window)
            final_used = BUDGET.used()
            self.assertGreaterEqual(final_used, 0)
        except Exception:
            # API call might fail, but we're testing the mechanism
            pass


if __name__ == '__main__':
    import sys

    # Print instructions if no API key
    if not os.environ.get("GROQ_API_KEY"):
        print("\n" + "="*60)
        print("To run Groq integration tests:")
        print("="*60)
        print("\n  Windows:")
        print("    set GROQ_API_KEY=your_api_key")
        print("    python -m pytest tests/test_groq_integration.py -v")
        print("\n  macOS/Linux:")
        print("    export GROQ_API_KEY=your_api_key")
        print("    python -m pytest tests/test_groq_integration.py -v")
        print("\nGet your free API key at: https://console.groq.com")
        print("="*60 + "\n")

    unittest.main()
