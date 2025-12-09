"""
Retail Insights Agent - GenAI-powered retail analytics.

Multi-agent system for natural language queries on retail sales data.
Built with Google ADK, DuckDB, PandasAI, and NVIDIA NeMo Guardrails.
"""

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

print("\n" + "="*60)
print("  RETAIL INSIGHTS AGENT - Startup")
print("="*60)

# Import config first to set up authentication
from . import config

# Eager load: Initialize DuckDB and load CSV tables at startup
from .database.duckdb import get_connection
get_connection()

# Import agents after database is ready
from .agents import root_agent

print("="*60)
print("  RETAIL INSIGHTS AGENT - Ready!")
print("="*60 + "\n")

# ADK entry point
__all__ = ["root_agent"]
