"""Utility helper functions."""

import re


def clip(text: str, n: int) -> str:
    """Collapse whitespace and hard-truncate text.

    Args:
        text: Text to clip
        n: Maximum length

    Returns:
        Clipped text
    """
    text = re.sub(r"\s+", " ", str(text or "")).strip()
    return text[:n]


def format_product_display(product: dict) -> str:
    """Format product data for display.

    Args:
        product: Product dictionary

    Returns:
        Formatted string
    """
    lines = []

    # Common field name variations
    product_id = product.get("product_id") or product.get("Product_ID")
    product_name = product.get("product_name") or product.get("Product_Name")
    category = product.get("category") or product.get("Category")
    hs_code = product.get("hsn_code") or product.get("HSN_Code")

    if product_id:
        lines.append(f"**Product ID**: {product_id}")
    if product_name:
        lines.append(f"**Name**: {product_name}")
    if category:
        lines.append(f"**Category**: {category}")
    if hs_code:
        lines.append(f"**HS Code**: {hs_code}")

    # Add any other fields
    for key, value in product.items():
        if key.lower() not in ["product_id", "product_name", "category", "hsn_code"]:
            lines.append(f"**{key}**: {value}")

    return "\n".join(lines)


def format_error(error: str) -> str:
    """Format an error message for display.

    Args:
        error: Error message

    Returns:
        Formatted error string
    """
    return f"⚠️ **Error**: {error}"


def validate_product_id(product_id: str) -> tuple[bool, str]:
    """Validate product ID input.

    Args:
        product_id: Product ID to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not product_id or not product_id.strip():
        return False, "Product ID cannot be empty"

    product_id = product_id.strip()

    if len(product_id) > 50:
        return False, "Product ID is too long (max 50 characters)"

    return True, ""


def validate_country(country: str) -> tuple[bool, str]:
    """Validate country input.

    Args:
        country: Country name to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not country or not country.strip():
        return False, "Country cannot be empty"

    country = country.strip()

    if len(country) > 100:
        return False, "Country name is too long"

    return True, ""


def safe_display(text: str, max_length: int = 5000) -> str:
    """Safely display text by truncating if needed.

    Args:
        text: Text to display
        max_length: Maximum length before truncation

    Returns:
        Safe text for display
    """
    if len(str(text)) > max_length:
        return str(text)[:max_length] + f"\n\n...[truncated - {len(str(text))} total chars]"
    return str(text)


def parse_compliance_response(response: str) -> dict:
    """Parse compliance response into structured format.

    Args:
        response: Raw response text

    Returns:
        Dictionary with parsed sections
    """
    sections = {
        "product_info": "",
        "documents": "",
        "duties": "",
        "payment_methods": "",
        "additional_info": response,
    }

    # Simple pattern matching for common sections
    patterns = {
        "product_info": r"(?:Product|product).*?(?=\n\n|\Z)",
        "documents": r"(?:Document|document|Required).*?(?=\n\n|\Z)",
        "duties": r"(?:Duty|Duties|duty).*?(?=\n\n|\Z)",
        "payment_methods": r"(?:Payment|payment).*?(?=\n\n|\Z)",
    }

    for section, pattern in patterns.items():
        match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)
        if match:
            sections[section] = match.group(0).strip()

    return sections
