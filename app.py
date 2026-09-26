"""Main Streamlit application for the Logistics Compliance Assistant."""

import streamlit as st
from streamlit_option_menu import option_menu
import os
from typing import Optional

from core.groq_client import create_llm, BUDGET
from core.agent import create_compliance_agent, invoke_agent, simple_compliance_lookup
from core.database import (
    get_product_by_id,
    search_products,
    get_database_info,
    check_database_exists,
)
from utils.helpers import (
    format_product_display,
    format_error,
    validate_product_id,
    validate_country,
    safe_display,
)


# Page configuration
st.set_page_config(
    page_title="Logistics Compliance Assistant",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
    <style>
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 20px;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 12px;
        border-radius: 4px;
        margin: 10px 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 12px;
        border-radius: 4px;
        margin: 10px 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 12px;
        border-radius: 4px;
        margin: 10px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def check_api_key() -> Optional[str]:
    """Check for Groq API key in secrets or environment."""
    # Try Streamlit secrets first
    try:
        api_key = st.secrets.get("groq_api_key")
        if api_key:
            return api_key
    except:
        pass

    # Try environment variable
    api_key = os.environ.get("GROQ_API_KEY")
    if api_key:
        return api_key

    return None


def check_database() -> bool:
    """Check if database exists and is accessible."""
    if not check_database_exists():
        st.error("❌ Database file not found!")
        return False
    return True


@st.cache_resource
def get_agent_and_llm(api_key: str):
    """Cache the agent and LLM instances."""
    agent = create_compliance_agent(api_key)
    return agent


def main():
    """Main application function."""
    # Header
    st.markdown(
        "<h1 style='text-align: center; color: #667eea;'>🌍 Logistics Compliance Assistant</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; color: #666;'>Find compliance requirements for international shipments</p>",
        unsafe_allow_html=True,
    )
    st.divider()

    # Check API key
    api_key = check_api_key()
    if not api_key:
        st.error(
            "❌ **Groq API Key not found!**\n\n"
            "Please add your API key:\n"
            "- **Local**: Create `.streamlit/secrets.toml` with `groq_api_key = \"your-key\"`\n"
            "- **Streamlit Cloud**: Add via Settings → Secrets\n\n"
            "Get a free key at https://console.groq.com"
        )
        st.stop()

    # Check database
    if not check_database():
        st.stop()

    # Sidebar navigation
    with st.sidebar:
        st.header("Navigation")
        selected = option_menu(
            "Menu",
            ["Compliance Lookup", "Product Search", "About", "Debug"],
            icons=["search", "database", "info-circle", "gear"],
            menu_icon="cast",
            default_index=0,
        )

    # Main content based on selection
    if selected == "Compliance Lookup":
        show_compliance_lookup(api_key)
    elif selected == "Product Search":
        show_product_search()
    elif selected == "About":
        show_about()
    elif selected == "Debug":
        show_debug(api_key)


def show_compliance_lookup(api_key: str):
    """Show the main compliance lookup interface."""
    st.header("🔍 Find Compliance Requirements")

    col1, col2, col3 = st.columns(3)

    with col1:
        product_id = st.text_input(
            "Product ID",
            placeholder="e.g., P001",
            help="Enter the product ID to look up",
        )

    with col2:
        source_country = st.text_input(
            "Source Country",
            placeholder="e.g., India",
            help="Country of origin",
        )

    with col3:
        destination_country = st.text_input(
            "Destination Country",
            placeholder="e.g., USA",
            help="Destination country",
        )

    # Advanced options
    with st.expander("⚙️ Advanced Options"):
        use_agent = st.checkbox(
            "Use ReAct Agent",
            value=True,
            help="Use AI agent for reasoning (slower but more comprehensive). "
            "Uncheck for faster simple lookup.",
        )

    # Validate inputs
    if st.button("🔎 Get Compliance Info", type="primary", use_container_width=True):
        # Strip whitespace from inputs
        product_id = product_id.strip()
        source_country = source_country.strip()
        destination_country = destination_country.strip()

        # Validate inputs
        is_valid_pid, pid_error = validate_product_id(product_id)
        if not is_valid_pid:
            st.error(f"❌ {pid_error}")
            return

        is_valid_src, src_error = validate_country(source_country)
        if not is_valid_src:
            st.error(f"❌ {src_error}")
            return

        is_valid_dst, dst_error = validate_country(destination_country)
        if not is_valid_dst:
            st.error(f"❌ {dst_error}")
            return

        # Get product details
        st.subheader("📦 Product Information")
        product = get_product_by_id(product_id)

        if not product:
            st.warning(f"⚠️ Product ID '{product_id}' not found in database.")
            st.info("Try searching for products using the 'Product Search' tab.")
            return

        # Display product info
        st.markdown(format_product_display(product))

        # Get compliance info
        st.subheader("📋 Compliance Requirements")

        with st.spinner(
            "Fetching compliance information... (this may take a moment)"
        ):
            try:
                if use_agent:
                    # Use ReAct agent
                    agent = get_agent_and_llm(api_key)
                    result = invoke_agent(agent, product_id, source_country, destination_country)
                else:
                    # Use simple lookup
                    result = simple_compliance_lookup(
                        api_key, product_id, source_country, destination_country
                    )

                st.markdown(safe_display(result))

                # Token budget info
                with st.expander("📊 Token Usage"):
                    st.info(
                        f"**Groq API Token Budget**\n\n"
                        f"- Tokens used (this minute): {BUDGET.used()}/{BUDGET.limit}\n"
                        f"- Free tier limit: 8,000 TPM\n"
                        f"- Safety margin: 80%"
                    )

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


def show_product_search():
    """Show the product search interface."""
    st.header("🔎 Search Products")

    search_type = st.radio(
        "Search by:",
        ["Product ID", "Product Name", "Category", "View All"],
        horizontal=True,
    )

    if search_type == "Product ID":
        product_id = st.text_input("Enter Product ID:")
        if product_id:
            product = get_product_by_id(product_id.strip())
            if product:
                st.subheader("Product Found")
                st.markdown(format_product_display(product))
            else:
                st.warning("Product not found")

    elif search_type == "Product Name":
        product_name = st.text_input("Enter Product Name (or partial name):")
        if product_name:
            results = search_products(product_name.strip())
            if results:
                st.subheader(f"Found {len(results)} product(s)")
                for product in results:
                    with st.expander(
                        product.get("product_name")
                        or product.get("Product_Name", "Unknown")
                    ):
                        st.markdown(format_product_display(product))
            else:
                st.warning("No products found")

    elif search_type == "Category":
        category = st.text_input("Enter Category:")
        if category:
            results = search_products(category.strip())
            if results:
                st.subheader(f"Found {len(results)} product(s)")
                for product in results:
                    with st.expander(
                        product.get("product_name")
                        or product.get("Product_Name", "Unknown")
                    ):
                        st.markdown(format_product_display(product))
            else:
                st.warning("No products found in this category")

    elif search_type == "View All":
        if st.button("Load All Products"):
            results = search_products("", limit=100)
            if results:
                st.subheader(f"Total Products: {len(results)}")
                for product in results:
                    with st.expander(
                        product.get("product_name")
                        or product.get("Product_Name", "Unknown")
                    ):
                        st.markdown(format_product_display(product))
            else:
                st.info("No products found")


def show_about():
    """Show the about page."""
    st.header("ℹ️ About")

    st.markdown(
        """
    ## Logistics Compliance Assistant

    This application helps supply chain and logistics managers quickly find compliance
    requirements for international shipments.

    ### Features
    - 📦 **Product Lookup**: Find product details by ID
    - 🔍 **Intelligent Search**: Uses Groq API + LangChain for intelligent compliance search
    - 📋 **Compliance Info**: Get import/export requirements, duties, and payment methods
    - ⚡ **Fast & Efficient**: Rate-limited API calls, optimized for free tier

    ### Technology Stack
    - **LLM**: [Groq API](https://groq.com) - blazing fast inference
    - **Framework**: [LangChain](https://langchain.com)
    - **Frontend**: [Streamlit](https://streamlit.io)
    - **Database**: SQLite (greatglobe.db)

    ### How It Works
    1. Enter a **Product ID** from the database
    2. Specify **Source** and **Destination** countries
    3. The app looks up product details and compliance requirements
    4. Results include required documents, duties, and payment obligations

    ### API Rate Limits
    - Free tier: 8,000 tokens per minute
    - Auto-retry on rate limits
    - ~80% safety margin to avoid throttling

    ### Get Your Groq API Key
    Visit [console.groq.com](https://console.groq.com) to get a free API key
    (no credit card required!)

    ### Support
    - [Groq Documentation](https://console.groq.com/docs)
    - [LangChain Documentation](https://python.langchain.com)
    - [Streamlit Documentation](https://docs.streamlit.io)
    """
    )


def show_debug(api_key: str):
    """Show debug information."""
    st.header("🔧 Debug Information")

    # Database info
    st.subheader("Database Status")
    db_info = get_database_info()

    col1, col2, col3 = st.columns(3)
    with col1:
        if db_info.get("exists"):
            st.success("✅ Database Found")
        else:
            st.error("❌ Database Not Found")

    with col2:
        st.info(f"📁 Path: `{db_info.get('path')}`")

    with col3:
        if "tables" in db_info:
            st.info(f"📊 Tables: {len(db_info['tables'])}")

    # Tables info
    if "tables" in db_info:
        st.subheader("Tables")
        for table in db_info["tables"]:
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**{table}**")
            with col2:
                count_key = f"{table}_count"
                if count_key in db_info:
                    st.write(f"Rows: {db_info[count_key]}")

    # API Status
    st.subheader("API Status")
    if api_key:
        st.success("✅ Groq API Key Configured")
    else:
        st.error("❌ Groq API Key Not Found")

    # Token budget
    st.subheader("Token Budget")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Used (this min)", BUDGET.used())
    with col2:
        st.metric("Limit", BUDGET.limit)
    with col3:
        pct = (BUDGET.used() / BUDGET.limit * 100) if BUDGET.limit > 0 else 0
        st.metric("Usage %", f"{pct:.1f}%")

    # Version info
    st.subheader("Version Information")
    st.text_input("Version", "1.0.0", disabled=True)


if __name__ == "__main__":
    main()
