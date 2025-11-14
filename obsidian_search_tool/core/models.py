"""Data models for Obsidian Search Tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class StatusResponse:
    """Response from status check.

    Attributes:
        status: Connection status (e.g., "connected")
        api_url: API base URL
        timestamp: ISO 8601 timestamp
        message: Human-readable message
    """

    status: str
    api_url: str
    timestamp: str
    message: str


@dataclass
class AuthResponse:
    """Response from authentication check.

    Attributes:
        status: Authentication status (e.g., "authenticated")
        api_url: API base URL
        timestamp: ISO 8601 timestamp
        message: Human-readable message
    """

    status: str
    api_url: str
    timestamp: str
    message: str


@dataclass
class SearchResponse:
    """Response from search operation.

    Attributes:
        success: Whether the search succeeded
        data: Search result data (if successful)
        error: Error information (if failed)
    """

    success: bool
    data: dict[str, Any] | None
    error: dict[str, Any] | None

    @property
    def query(self) -> str:
        """Get the query string from response data."""
        if self.data:
            return str(self.data.get("query", ""))
        return ""

    @property
    def search_type(self) -> str:
        """Get the search type from response data."""
        if self.data:
            return str(self.data.get("search_type", ""))
        return ""

    @property
    def timestamp(self) -> str:
        """Get the timestamp from response data."""
        if self.data:
            return str(self.data.get("timestamp", ""))
        return ""

    @property
    def results(self) -> list[dict[str, Any]]:
        """Get the results list from response data."""
        if self.data and "results" in self.data:
            results = self.data["results"]
            if isinstance(results, list):
                return results
        return []

    @property
    def result_count(self) -> int:
        """Get the number of results."""
        return len(self.results)
