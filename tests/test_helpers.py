"""Unit tests for helper functions."""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.helpers import (
    clip,
    validate_product_id,
    validate_country,
    format_product_display,
    safe_display,
)


class TestClipFunction(unittest.TestCase):
    """Test the clip helper function."""

    def test_clip_short_text(self):
        """Test clipping text shorter than limit."""
        text = "Hello"
        result = clip(text, 100)
        self.assertEqual(result, "Hello")

    def test_clip_exact_length(self):
        """Test clipping text at exact length."""
        text = "Hello"
        result = clip(text, 5)
        self.assertEqual(result, "Hello")

    def test_clip_long_text(self):
        """Test clipping text longer than limit."""
        text = "Hello World"
        result = clip(text, 5)
        self.assertEqual(result, "Hello")

    def test_clip_whitespace_collapse(self):
        """Test that multiple whitespaces are collapsed."""
        text = "Hello    World   !"
        result = clip(text, 100)
        self.assertEqual(result, "Hello World !")

    def test_clip_leading_trailing_whitespace(self):
        """Test that leading/trailing whitespace is removed."""
        text = "   Hello World   "
        result = clip(text, 100)
        self.assertEqual(result, "Hello World")

    def test_clip_empty_string(self):
        """Test clipping empty string."""
        result = clip("", 10)
        self.assertEqual(result, "")


class TestValidateProductId(unittest.TestCase):
    """Test product ID validation."""

    def test_valid_product_id(self):
        """Test validating a valid product ID."""
        valid, error = validate_product_id("P001")
        self.assertTrue(valid)
        self.assertEqual(error, "")

    def test_empty_product_id(self):
        """Test validating empty product ID."""
        valid, error = validate_product_id("")
        self.assertFalse(valid)
        self.assertNotEqual(error, "")

    def test_whitespace_only_product_id(self):
        """Test validating whitespace-only product ID."""
        valid, error = validate_product_id("   ")
        self.assertFalse(valid)
        self.assertNotEqual(error, "")

    def test_long_product_id(self):
        """Test validating very long product ID."""
        long_id = "A" * 60
        valid, error = validate_product_id(long_id)
        self.assertFalse(valid)
        self.assertIn("too long", error.lower())

    def test_product_id_with_spaces(self):
        """Test product ID with spaces gets trimmed."""
        valid, error = validate_product_id("  P001  ")
        self.assertTrue(valid)


class TestValidateCountry(unittest.TestCase):
    """Test country name validation."""

    def test_valid_country(self):
        """Test validating valid country."""
        valid, error = validate_country("United States")
        self.assertTrue(valid)
        self.assertEqual(error, "")

    def test_single_word_country(self):
        """Test single-word country name."""
        valid, error = validate_country("India")
        self.assertTrue(valid)
        self.assertEqual(error, "")

    def test_empty_country(self):
        """Test empty country."""
        valid, error = validate_country("")
        self.assertFalse(valid)
        self.assertNotEqual(error, "")

    def test_whitespace_country(self):
        """Test whitespace-only country."""
        valid, error = validate_country("   ")
        self.assertFalse(valid)
        self.assertNotEqual(error, "")

    def test_long_country_name(self):
        """Test very long country name."""
        long_name = "A" * 150
        valid, error = validate_country(long_name)
        self.assertFalse(valid)

    def test_country_with_special_chars(self):
        """Test country with special characters."""
        valid, error = validate_country("São Tomé")
        self.assertTrue(valid)


class TestFormatProductDisplay(unittest.TestCase):
    """Test product formatting for display."""

    def test_format_empty_product(self):
        """Test formatting empty product dict."""
        result = format_product_display({})
        self.assertIsInstance(result, str)

    def test_format_simple_product(self):
        """Test formatting simple product."""
        product = {
            'product_id': 'P001',
            'product_name': 'Test Product',
            'category': 'Test Category'
        }
        result = format_product_display(product)
        self.assertIn('P001', result)
        self.assertIn('Test Product', result)
        self.assertIn('Test Category', result)

    def test_format_product_field_variants(self):
        """Test formatting with different field name variants."""
        product = {
            'Product_ID': 'P001',
            'Product_Name': 'Test',
            'Category': 'Cat'
        }
        result = format_product_display(product)
        self.assertIn('P001', result)
        self.assertIn('Test', result)


class TestSafeDisplay(unittest.TestCase):
    """Test safe display function."""

    def test_safe_display_short_text(self):
        """Test safe display with short text."""
        text = "Hello"
        result = safe_display(text, max_length=100)
        self.assertEqual(result, "Hello")

    def test_safe_display_long_text(self):
        """Test safe display with long text."""
        text = "A" * 10000
        result = safe_display(text, max_length=1000)
        self.assertIn("truncated", result.lower())
        self.assertLess(len(result), len(text) + 100)

    def test_safe_display_exact_length(self):
        """Test safe display at exact max length."""
        text = "A" * 1000
        result = safe_display(text, max_length=1000)
        self.assertNotIn("truncated", result)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases in helper functions."""

    def test_clip_with_newlines(self):
        """Test clip with newline characters."""
        text = "Hello\n\nWorld"
        result = clip(text, 100)
        self.assertEqual(result, "Hello World")

    def test_clip_with_tabs(self):
        """Test clip with tab characters."""
        text = "Hello\t\tWorld"
        result = clip(text, 100)
        self.assertEqual(result, "Hello World")

    def test_validate_with_unicode(self):
        """Test validation with unicode characters."""
        valid, error = validate_country("中国")  # China in Chinese
        self.assertTrue(valid)

    def test_format_with_none_values(self):
        """Test formatting product with None values."""
        product = {
            'product_id': 'P001',
            'description': None,
            'price': None
        }
        result = format_product_display(product)
        self.assertIsInstance(result, str)


if __name__ == '__main__':
    unittest.main()
