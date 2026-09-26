"""LangChain tools setup for the logistics assistant."""

from typing import Dict, Any

from langchain_core.tools import tool
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from ddgs import DDGS

from core.database import execute_query, DB_PATH


def create_sql_toolkit() -> SQLDatabaseToolkit:
    """Create a SQL database toolkit for querying product information."""
    db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")
    return SQLDatabaseToolkit(db=db, llm=None)  # LLM will be injected later


@tool
def web_search(query: str, max_results: int = 5) -> str:
    """Search the web using DuckDuckGo for compliance information.

    Args:
        query: Search query
        max_results: Maximum number of results to return

    Returns:
        Formatted search results
    """
    try:
        results = DDGS().text(query, max_results=max_results)
        if not results:
            return "No search results found."

        formatted_results = []
        for i, result in enumerate(results, 1):
            formatted_results.append(
                f"{i}. {result.get('title', 'N/A')}\n"
                f"   URL: {result.get('href', 'N/A')}\n"
                f"   Snippet: {result.get('body', 'N/A')[:500]}"
            )

        return "\n\n".join(formatted_results)
    except Exception as e:
        return f"Search error: {str(e)}"


@tool
def product_lookup(product_id: str) -> str:
    """Look up product details from the database.

    Args:
        product_id: The product ID to look up

    Returns:
        Formatted product information
    """
    try:
        results = execute_query(
            "SELECT * FROM products WHERE product_id = ? OR Product_ID = ? LIMIT 1",
            (product_id, product_id)
        )

        if not results:
            return f"Product {product_id} not found in database."

        product = results[0]
        lines = [f"Product ID: {product.get('product_id', product.get('Product_ID', 'N/A'))}"]

        for key, value in product.items():
            if key not in ['product_id', 'Product_ID']:
                lines.append(f"{key}: {value}")

        return "\n".join(lines)
    except Exception as e:
        return f"Error looking up product: {str(e)}"


@tool
def compliance_search(hs_code: str, destination_country: str) -> str:
    """Search for compliance requirements based on HS code and destination country.

    Args:
        hs_code: Harmonized System code
        destination_country: Destination country for import requirements

    Returns:
        Compliance information
    """
    query = (
        f"Import requirements for HS code {hs_code} to {destination_country}. "
        f"Include duties, documents, and tariffs."
    )
    return web_search(query, max_results=5)


def get_tools_list():
    """Get list of tools for the agent."""
    return [product_lookup, web_search, compliance_search]
