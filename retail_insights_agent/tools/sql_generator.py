"""
SQL generation tool for ADK agents.

Used by Query Resolution Agent to convert natural language to SQL.
"""

import logging

from ..database.pandasai import get_generator

logger = logging.getLogger(__name__)


def generate_sql(question: str) -> dict:
    """
    Generate SQL from a natural language question.

    Args:
        question: Natural language question about retail data

    Returns:
        Dict with status, sql, and message
    """
    if not question or not question.strip():
        return {
            "status": "error",
            "sql": None,
            "message": "Empty question provided",
        }

    logger.info(f"Generating SQL for: {question[:50]}...")

    try:
        generator = get_generator()
        result = generator.generate(question)

        if result.success and result.sql:
            return {
                "status": "success",
                "sql": result.sql,
                "message": f"Generated SQL for: {question}",
            }
        else:
            return {
                "status": "error",
                "sql": None,
                "message": result.error or "Failed to generate SQL",
            }

    except Exception as e:
        logger.error(f"SQL generation failed: {e}")
        return {
            "status": "error",
            "sql": None,
            "message": str(e),
        }
