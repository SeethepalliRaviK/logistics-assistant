"""Pytest configuration and shared fixtures."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest


@pytest.fixture
def sample_product():
    """Sample product for testing."""
    return {
        'product_id': 'P001',
        'product_name': 'Test Product',
        'category': 'Test Category',
        'hsn_code': '123456',
    }


@pytest.fixture
def sample_products():
    """Multiple sample products for testing."""
    return [
        {
            'product_id': 'P001',
            'product_name': 'Product A',
            'category': 'Electronics',
            'hsn_code': '123456',
        },
        {
            'product_id': 'P002',
            'product_name': 'Product B',
            'category': 'Textiles',
            'hsn_code': '234567',
        },
    ]


def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
