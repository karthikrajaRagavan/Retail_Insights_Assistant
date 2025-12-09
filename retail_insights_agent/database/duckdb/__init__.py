"""DuckDB in-memory database for analytical queries."""

from .connection import DuckDBConnection, get_connection
from .executor import execute_query, QueryResult
