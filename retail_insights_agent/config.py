"""
Centralized configuration for Retail Insights Agent.

All settings in one place for easy management and environment overrides.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Paths
BASE_DIR = Path(__file__).parent  # retail_insights_agent/
REPO_ROOT = BASE_DIR.parent       # repo root (where .env lives)
DATA_DIR = BASE_DIR / "data"

# Load .env from repo root
load_dotenv(REPO_ROOT / ".env")


# Google Cloud / Vertex AI Authentication
# User can specify their own JSON file name via env, or use default
SERVICE_ACCOUNT_FILE = REPO_ROOT / os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "service-account.json")
if SERVICE_ACCOUNT_FILE.exists():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(SERVICE_ACCOUNT_FILE)

# Set Vertex AI environment variables for ADK
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", os.getenv("GOOGLE_CLOUD_PROJECT", ""))
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"))


# LLM - OpenAI (PandasAI + NeMo Guardrails)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

# LLM - Gemini (ADK Agents)
ORCHESTRATOR_MODEL = os.getenv("ORCHESTRATOR_MODEL", "gemini-2.5-pro")      # Root agent
PIPELINE_AGENT_MODEL = os.getenv("PIPELINE_AGENT_MODEL", "gemini-2.5-flash")  # Sub-agents in QA pipeline


# Guardrails
GUARDRAILS_BLOCKED_MESSAGE = """I'm focused on retail sales analytics. If you have questions about sales data, I'm here to help."""


# Table Schema - Amazon Sales
TABLE_SCHEMAS = {
    "amazon_sales": {
        "source_file": "Amazon Sale Report.csv",
        "description": "Amazon India order transactions (128K rows, Apr-Jun 2022)",
        "column_mapping": {
            "Order ID": "order_id",
            "Date": "order_date",
            "Status": "status",
            "Fulfilment": "fulfilment",
            "Style": "style",
            "SKU": "sku",
            "Category": "category",
            "Size": "size",
            "Qty": "quantity",
            "Amount": "amount",
            "ship-city": "city",
            "ship-state": "state",
            "B2B": "is_b2b",
        },
        "field_descriptions": {
            "order_id": "Unique Amazon order identifier",
            "order_date": "Order date (MM-DD-YY format)",
            "status": "Order status: Shipped, Cancelled, Pending, Delivered, etc.",
            "fulfilment": "Fulfilment type: Amazon or Merchant",
            "style": "Product style code",
            "sku": "Stock keeping unit",
            "category": "Product category: kurta, Set, Top, Western Dress, Blouse, etc.",
            "size": "Product size: XS, S, M, L, XL, XXL, 3XL, etc.",
            "quantity": "Quantity ordered",
            "amount": "Order amount in INR (null for cancelled orders)",
            "city": "Shipping city",
            "state": "Shipping state (Indian states)",
            "is_b2b": "Business-to-business order flag (True/False)",
        },
    },
}


def get_schema_summary() -> str:
    """Get human-readable schema summary for agent instructions."""
    lines = []
    for table_name, schema in TABLE_SCHEMAS.items():
        cols = list(schema["column_mapping"].values())
        lines.append(f"- {table_name}: {schema['description']}")
        lines.append(f"  Columns: {', '.join(cols[:8])}...")
    return "\n".join(lines)
