"""LangChain tools setup for the logistics assistant."""

from typing import Dict, Any

from langchain_core.tools import Tool
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from ddgs import DDGS

from core.database import execute_query, DB_PATH


def create_sql_toolkit() -> SQLDatabaseToolkit:
    """Create a SQL database toolkit for querying product information."""
    db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")
    return SQLDatabaseToolkit(db=db, llm=None)  # LLM will be injected later


def web_search_tool(query: str, max_results: int = 5) -> str:
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


def product_lookup_tool(product_id: str) -> str:
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


def compliance_search_tool(hs_code: str, source_country: str, destination_country: str) -> str:
    """Search for compliance requirements based on HS code and countries.

    Args:
        hs_code: Harmonized System code
        source_country: Country of origin
        destination_country: Destination country

    Returns:
        Compliance information
    """
    query = (
        f"Import/export requirements for HS code {hs_code} "
        f"shipping from {source_country} to {destination_country}"
    )
    return web_search_tool(query, max_results=5)


def create_tools_dict() -> Dict[str, Tool]:
    """Create a dictionary of tools for the agent.

    Returns:
        Dictionary mapping tool names to Tool instances
    """
    tools = {
        "product_lookup": Tool(
            name="Product Lookup",
            func=product_lookup_tool,
            description=(
                "Look up product details from the database using Product ID. "
                "Returns product name, category, HSN code, and other details."
            ),
        ),
        "web_search": Tool(
            name="Web Search",
            func=web_search_tool,
            description=(
                "Search the web using DuckDuckGo for information about import/export "
                "compliance, duties, documents, and payment methods. Use specific terms "
                "like 'HS code', 'import requirements', 'customs', etc."
            ),
        ),
        "compliance_search": Tool(
            name="Compliance Search",
            func=compliance_search_tool,
            description=(
                "Search for compliance requirements for a specific HS code between "
                "source and destination countries. Returns import/export documents, "
                "duties, and payment obligations."
            ),
        ),
    }

    return tools


def get_tools_list():
    """Get list of tools for the agent."""
    tools_dict = create_tools_dict()
    return list(tools_dict.values())
