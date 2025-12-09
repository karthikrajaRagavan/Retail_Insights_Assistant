"""
ADK Entry Point.

This file exports the root_agent for ADK CLI.
Run with: adk web
"""

from .agents import root_agent

# Re-export for ADK
__all__ = ["root_agent"]
