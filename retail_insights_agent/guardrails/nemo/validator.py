"""
Input validation using NVIDIA NeMo Guardrails.

Validates user queries before processing by the agent.
"""

import re
import logging
import asyncio
from typing import Optional
from dataclasses import dataclass

from nemoguardrails import LLMRails, RailsConfig

from .config import RAILS_YAML, RAILS_COLANG, BLOCK_PATTERNS
from ...config import GUARDRAILS_BLOCKED_MESSAGE

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result from input validation."""

    allowed: bool
    message: str
    reason: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "allowed": self.allowed,
            "message": self.message,
            "reason": self.reason,
        }


class InputValidator:
    """
    Validates user input using NeMo Guardrails.

    Combines fast regex pattern matching with LLM-based policy checking.
    """

    def __init__(self):
        self._patterns = [re.compile(p) for p in BLOCK_PATTERNS]

    def _quick_pattern_check(self, query: str) -> Optional[str]:
        """Fast pattern matching before LLM call."""
        for pattern in self._patterns:
            if pattern.search(query):
                return f"Blocked by pattern: {pattern.pattern}"
        return None

    def _create_rails(self) -> LLMRails:
        """Create NeMo Guardrails instance."""
        return LLMRails(
            RailsConfig.from_content(
                colang_content=RAILS_COLANG,
                yaml_content=RAILS_YAML,
            )
        )

    async def check_async(self, query: str) -> ValidationResult:
        """
        Validate query asynchronously.

        Args:
            query: User's input query

        Returns:
            ValidationResult with allowed status and message
        """
        # Quick pattern check
        pattern_match = self._quick_pattern_check(query)
        if pattern_match:
            logger.info(f"Query blocked by pattern: {query[:50]}...")
            return ValidationResult(
                allowed=False,
                message=GUARDRAILS_BLOCKED_MESSAGE,
                reason=pattern_match,
            )

        # LLM-based check
        try:
            rails = self._create_rails()
            result = await rails.generate_async(
                messages=[{"role": "user", "content": query}],
                options={"rails": ["input"]}
            )

            # Check if blocked
            response = ""
            if result.response and len(result.response) > 0:
                response = result.response[0].get("content", "")

            is_blocked = response.startswith("I can only help with")

            if is_blocked:
                logger.info(f"Query blocked by LLM: {query[:50]}...")
                return ValidationResult(
                    allowed=False,
                    message=GUARDRAILS_BLOCKED_MESSAGE,
                    reason="Policy violation",
                )

            return ValidationResult(allowed=True, message=query)

        except Exception as e:
            logger.error(f"Guardrail check failed: {e}")
            # Fail open - allow query if guardrails fail
            return ValidationResult(
                allowed=True,
                message=query,
                reason=f"Guardrail error (fail-open): {str(e)}",
            )

    def check(self, query: str) -> ValidationResult:
        """
        Validate query synchronously.

        Args:
            query: User's input query

        Returns:
            ValidationResult with allowed status and message
        """
        try:
            loop = asyncio.get_running_loop()
            # In async context - use thread
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, self.check_async(query))
                return future.result(timeout=30)
        except RuntimeError:
            # No running loop
            return asyncio.run(self.check_async(query))


# Module-level convenience function
def validate_query(query: str) -> ValidationResult:
    """Validate a query using the default validator."""
    validator = InputValidator()
    return validator.check(query)
