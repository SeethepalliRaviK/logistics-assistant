"""ReAct agent for the logistics compliance assistant."""

from typing import Optional

from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage, HumanMessage

from core.groq_client import create_llm, safe_llm_call
from core.tools import get_tools_list
from core import USE_AGENT, AGENT_RECURSION_LIMIT


SYSTEM_PROMPT = """You are a logistics compliance assistant for Greatglobe Logistics.
Your role is to help supply chain managers quickly find and understand import/export
compliance requirements for shipments.

When a user provides a Product ID and source/destination countries:
1. First, look up the product details using the product_lookup tool to get the HSN code
2. Then search for compliance requirements using the compliance_search or web_search tool
3. Summarize the findings in a clear, structured format

Always provide:
- Product details (name, category, HSN code)
- Required import/export documents
- Duty information
- Payment methods and obligations
- Any additional compliance notes

Be precise and cite sources when available."""


def create_compliance_agent(groq_api_key: str):
    """Create a ReAct agent for compliance queries.

    Args:
        groq_api_key: The Groq API key

    Returns:
        Compiled ReAct agent
    """
    llm = create_llm(groq_api_key)
    tools = get_tools_list()

    agent_executor = create_react_agent(
        model=llm,
        tools=tools,
        state_modifier=SYSTEM_PROMPT,
        debug=False,
    )

    return agent_executor


def invoke_agent(agent, product_id: str, source_country: str, destination_country: str) -> str:
    """Invoke the agent with a compliance query.

    Args:
        agent: The compiled agent executor
        product_id: Product ID to look up
        source_country: Country of origin
        destination_country: Destination country

    Returns:
        Agent response with compliance information
    """
    query = (
        f"I need compliance information for Product ID: {product_id}\n"
        f"Shipping from: {source_country}\n"
        f"Destination: {destination_country}\n\n"
        f"Please look up the product details, then find the compliance requirements "
        f"including import/export documents, duties, and payment methods."
    )

    try:
        result = agent.invoke(
            {"messages": [HumanMessage(content=query)]},
            config={"recursion_limit": AGENT_RECURSION_LIMIT}
        )

        # Extract the final message
        if result and "messages" in result:
            messages = result["messages"]
            if messages:
                final_message = messages[-1]
                if hasattr(final_message, "content"):
                    return final_message.content

        return "Unable to retrieve compliance information. Please try again."

    except Exception as e:
        return f"Error processing request: {str(e)}"


def simple_compliance_lookup(groq_api_key: str, product_id: str,
                             source_country: str, destination_country: str) -> str:
    """Simple lookup without agent (faster, cheaper).

    Args:
        groq_api_key: Groq API key
        product_id: Product ID
        source_country: Source country
        destination_country: Destination country

    Returns:
        Compliance information
    """
    from core.database import execute_query
    from core.tools import product_lookup_tool, compliance_search_tool

    # Step 1: Look up product
    product_info = product_lookup_tool(product_id)

    if "not found" in product_info.lower():
        return product_info

    # Step 2: Get HS code (try different field names)
    hs_code = None
    try:
        results = execute_query(
            "SELECT hsn_code FROM products WHERE product_id = ? OR Product_ID = ? LIMIT 1",
            (product_id, product_id)
        )
        if results:
            hs_code = results[0].get("hsn_code", results[0].get("HSN_Code"))
    except:
        pass

    # Step 3: Search compliance requirements
    if hs_code:
        compliance_info = compliance_search_tool(hs_code, source_country, destination_country)
    else:
        compliance_info = compliance_search_tool(product_id, source_country, destination_country)

    # Combine results
    return f"Product Information:\n{product_info}\n\n" \
           f"Compliance Requirements:\n{compliance_info}"
