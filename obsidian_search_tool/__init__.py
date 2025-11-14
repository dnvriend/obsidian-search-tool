"""Obsidian Search Tool - Search your Obsidian vault via CLI.

A command-line tool for searching an Obsidian vault through the Obsidian
Local REST API using Dataview Query Language (DQL) - TABLE queries only -
and JsonLogic queries.

This package provides both a CLI interface and a Python library for
programmatic access to Obsidian search operations.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

__version__ = "0.1.0"

# Public API exports for library usage
from obsidian_search_tool.core.client import (
    ObsidianAPIError,
    ObsidianAuthError,
    ObsidianClient,
    ObsidianClientError,
    ObsidianConnectionError,
)
from obsidian_search_tool.core.models import AuthResponse, SearchResponse, StatusResponse

__all__ = [
    # Version
    "__version__",
    # Client
    "ObsidianClient",
    # Exceptions
    "ObsidianClientError",
    "ObsidianAuthError",
    "ObsidianConnectionError",
    "ObsidianAPIError",
    # Models
    "StatusResponse",
    "AuthResponse",
    "SearchResponse",
]
