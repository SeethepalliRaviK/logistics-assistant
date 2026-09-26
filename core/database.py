"""Database operations for product and compliance information."""

import sqlite3
from typing import Optional, Dict, Any, List
from pathlib import Path


DB_PATH = Path(__file__).parent.parent / "data" / "greatglobe.db"


def get_connection():
    """Create and return a database connection."""
    return sqlite3.connect(str(DB_PATH))


def get_product_by_id(product_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve product details by Product ID.

    Args:
        product_id: The unique product identifier

    Returns:
        Dictionary with product details or None if not found
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM products
            WHERE product_id = ? OR Product_ID = ?
            LIMIT 1
            """,
            (product_id, product_id)
        )

        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        # Get column names
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(products)")
        columns = [col[1] for col in cursor.fetchall()]
        conn.close()

        return dict(zip(columns, row))

    except Exception as e:
        print(f"Database error fetching product {product_id}: {e}")
        return None


def get_all_products(limit: int = 100) -> List[Dict[str, Any]]:
    """Retrieve all products from database.

    Args:
        limit: Maximum number of products to return

    Returns:
        List of product dictionaries
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("PRAGMA table_info(products)")
        columns = [col[1] for col in cursor.fetchall()]

        cursor.execute(f"SELECT * FROM products LIMIT {limit}")
        rows = cursor.fetchall()
        conn.close()

        return [dict(zip(columns, row)) for row in rows]

    except Exception as e:
        print(f"Database error fetching products: {e}")
        return []


def search_products(search_term: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Search products by name or category.

    Args:
        search_term: Term to search for
        limit: Maximum results to return

    Returns:
        List of matching product dictionaries
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("PRAGMA table_info(products)")
        columns = [col[1] for col in cursor.fetchall()]

        search_pattern = f"%{search_term}%"
        cursor.execute(
            """
            SELECT * FROM products
            WHERE product_name LIKE ?
               OR Product_Name LIKE ?
               OR category LIKE ?
               OR Category LIKE ?
            LIMIT ?
            """,
            (search_pattern, search_pattern, search_pattern, search_pattern, limit)
        )

        rows = cursor.fetchall()
        conn.close()

        return [dict(zip(columns, row)) for row in rows]

    except Exception as e:
        print(f"Database error searching products: {e}")
        return []


def get_tables():
    """Get list of all tables in database."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tables
    except Exception as e:
        print(f"Database error listing tables: {e}")
        return []


def get_table_schema(table_name: str) -> List[tuple]:
    """Get column information for a table."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        schema = cursor.fetchall()
        conn.close()
        return schema
    except Exception as e:
        print(f"Database error getting schema: {e}")
        return []


def execute_query(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """Execute a raw SQL query (read-only for safety).

    Args:
        query: SQL SELECT query to execute
        params: Query parameters for safe substitution

    Returns:
        List of result dictionaries
    """
    # Only allow SELECT queries for safety
    if not query.strip().upper().startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed")

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)

        # Get column names from cursor description
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        conn.close()

        return [dict(zip(columns, row)) for row in rows]

    except Exception as e:
        print(f"Database query error: {e}")
        return []


def check_database_exists() -> bool:
    """Check if database file exists and is accessible."""
    return DB_PATH.exists()


def get_database_info() -> Dict[str, Any]:
    """Get information about the database."""
    if not check_database_exists():
        return {"exists": False, "path": str(DB_PATH)}

    try:
        tables = get_tables()
        info = {
            "exists": True,
            "path": str(DB_PATH),
            "tables": tables,
        }

        # Get row counts for each table
        for table in tables:
            try:
                results = execute_query(f"SELECT COUNT(*) as count FROM {table}")
                if results:
                    info[f"{table}_count"] = results[0].get("count", 0)
            except:
                pass

        return info
    except Exception as e:
        return {"exists": True, "path": str(DB_PATH), "error": str(e)}
